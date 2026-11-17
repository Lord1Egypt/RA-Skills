#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
phone-mark-query — 号码标记一键查询（九大平台聚合）

查询手机号 / 带区号固话在 电话邦、小米、360、腾讯、百度、泰迪熊、联通管家、
搜狗号码通、移动高频 九大平台的标记情况，自动汇总风险等级（高风险 / 营销骚扰 /
无标记 / 其他标记）并给出接听建议。

用法:
    python query.py <号码> [--json]
    python query.py --status
    python query.py --set-limit N

仅依赖 Python 3 标准库。状态文件: ~/.phone-mark-query/state.json
"""

import argparse
import datetime as _dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

# ================== 部署方配置区 ==================
# 查询接口（已配置；如需更换，改这里或用环境变量 PHONE_MARK_API_URL 覆盖）
API_URL = "http://glm_autoclaw.tongxinsys.cn:8088/HMBJ/ApiShiGlmAutoClaw"
# =================================================

ENV_API_URL = "PHONE_MARK_API_URL"        # 临时覆盖接口地址
ENV_DAILY_LIMIT = "PHONE_MARK_DAILY_LIMIT"  # 临时覆盖每日免费次数
ENV_STATE_DIR = "PHONE_MARK_STATE_DIR"    # 内部：测试用状态目录覆盖
DEFAULT_DAILY_LIMIT = 10
TIMEOUT_SECONDS = 15
MAX_ATTEMPTS = 2
UA = "phone-mark-query-skill/1.0"


def _state_dir():
    env = os.environ.get(ENV_STATE_DIR, "").strip()
    return Path(env) if env else (Path.home() / ".phone-mark-query")


STATE_DIR = _state_dir()
STATE_FILE = STATE_DIR / "state.json"

# 九大平台: 接口字段 -> 展示名
PLATFORMS = [
    ("dianhuabang", "电话邦"),
    ("xiaomi", "小米"),
    ("sanliuling", "360"),
    ("tengxun", "腾讯"),
    ("baidu", "百度"),
    ("taidixiong", "泰迪熊"),
    ("ltgj", "联通管家"),
    ("sghmt", "搜狗号码通"),
    ("yidonggaopin", "移动高频"),
]

# 风险关键词（按优先级从高到低；命中即定级）
RISK_RULES = [
    ("高风险", ["诈骗", "高风险", "骗", "违法", "犯罪", "赌博", "催收", "威胁",
               "敲诈", "冒充", "洗钱"]),
    ("营销/骚扰", ["骚扰", "广告", "推销", "营销", "中介", "房产", "教育", "培训",
                 "贷款", "办贷", "保险", "投资", "理财", "股票", "证券", "信用卡",
                 "办证", "招聘", "猎头", "促销", "会员", "快递", "外卖", "送餐",
                 "跑腿", "同城", "客服", "售后", "回访", "调研", "问卷", "宽带",
                 "流量", "话费", "银行", "装修", "搬家", "二手车"]),
]

ADVICE = {
    "高风险": "建议直接拒接并拉黑。切勿透露身份证、银行卡、验证码等信息；可拨打 96110 咨询或向 12321 举报。",
    "营销/骚扰": "如近期没有相关业务需求（看房/贷款/培训/快递等），建议拒接或静音处理；确需接听时先核实对方身份。",
    "其他标记": "号码在部分平台有标记但未能归类，建议谨慎接听，先核实对方身份再沟通。",
    "无标记": "九大平台均无标记，大概率是正常号码（新号码或低频呼叫也可能无标记），可正常接听。",
}


# ---------------- 号码规范化 ----------------

def normalize_phone(raw):
    """清理并校验号码：支持 11 位手机号（1 开头）或带区号固话（0 开头 10~12 位）。"""
    s = re.sub(r"[\s\-()（）]", "", str(raw or "").strip())
    if s.startswith("+86"):
        s = s[3:]
    elif s.startswith("86") and len(s) == 13 and s[2] == "1":
        s = s[2:]
    if re.fullmatch(r"1[3-9]\d{9}", s):
        return s
    if re.fullmatch(r"0\d{9,11}", s):
        return s
    raise ValueError(
        "号码格式不正确：支持 11 位手机号（1 开头）或带区号的固话（0 开头 10~12 位），"
        "例如 13800138000 或 031168179468")


# ---------------- 本地状态（uid + 每日额度） ----------------

def load_state():
    data = {}
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            data = {}
    except Exception:
        data = {}
    if not data.get("uid"):
        data["uid"] = str(uuid.uuid4())  # 每台机器首次运行生成，持久保存
    today = _dt.date.today().isoformat()
    if data.get("date") != today:
        data["date"] = today
        data["used"] = 0
    data.setdefault("used", 0)
    data.setdefault("daily_limit", DEFAULT_DAILY_LIMIT)
    return data


def save_state(data):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                          encoding="utf-8")


def effective_limit(data):
    """优先级: 环境变量 > 本地配置(state.json 的 daily_limit) > 默认 10"""
    env = os.environ.get(ENV_DAILY_LIMIT, "").strip()
    if env.isdigit() and int(env) > 0:
        return int(env)
    try:
        v = int(data.get("daily_limit", DEFAULT_DAILY_LIMIT))
        if v > 0:
            return v
    except (TypeError, ValueError):
        pass
    return DEFAULT_DAILY_LIMIT


# ---------------- 接口请求 ----------------

def http_get_json(url):
    last_err = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
                raw = resp.read().decode("utf-8", "replace")
            return json.loads(raw)
        except (urllib.error.URLError, TimeoutError, OSError,
                json.JSONDecodeError) as e:
            last_err = e
            if attempt < MAX_ATTEMPTS:
                time.sleep(1.5)
    raise RuntimeError("接口请求失败（已重试 %d 次）: %s" % (MAX_ATTEMPTS, last_err))


# ---------------- 解析与汇总 ----------------

def parse_field(value):
    """解析单个平台的标记值。
    返回 (marked, label, count, raw):
      marked=True  -> label 为标记内容, count 为标记人数（如有）
      marked=False -> 无标记
      marked=None  -> 未知格式, raw 原样返回
    """
    v = str(value or "").strip()
    low = v.lower()
    if low.startswith("yes"):
        parts = [p for p in re.split(r"[-－]", v[3:]) if p]
        count = None
        if len(parts) > 1 and re.fullmatch(r"\d+", parts[-1]):
            count = parts[-1]
            parts = parts[:-1]
        return True, "-".join(parts) or "有标记", count, v
    if low.startswith("no"):
        return False, "", None, v
    return None, v or "未知", None, v


def build_report(phone, data, state, limit):
    platforms = []
    for key, name in PLATFORMS:
        marked, label, count, raw = parse_field(data.get(key))
        platforms.append({"name": name, "marked": marked, "label": label,
                          "count": count, "raw": raw})
    marked_list = [p for p in platforms if p["marked"] is True]
    level, hits = "无标记", []
    if marked_list:
        level, hits = "其他标记", []
        text = " ".join(p["label"] or "" for p in marked_list)
        for lv, kws in RISK_RULES:
            hit = sorted({k for k in kws if k in text})
            if hit:
                level, hits = lv, hit
                break
    return {
        "phone": phone,
        "respid": str(data.get("respid", "")),
        "queried_at": _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "marked_count": len(marked_list),
        "platform_total": len(PLATFORMS),
        "platforms": platforms,
        "risk_level": level,
        "risk_keywords": hits,
        "advice": ADVICE.get(level, ADVICE["其他标记"]),
        "used": int(state.get("used", 0)),
        "limit": int(limit),
        "uid": str(state.get("uid", "")),
    }


# ---------------- 输出渲染 ----------------

def _w(s):
    return sum(2 if ord(ch) > 0x2E7F else 1 for ch in s)


def _table(rows, headers):
    """渲染 Unicode 表格（CJK 宽度对齐）。rows: [(平台, 标记情况), ...]"""
    all_rows = [headers] + list(rows)
    w1 = max(_w(a) for a, _ in all_rows)
    w2 = max(_w(b) for _, b in all_rows)
    top = "┌" + "─" * (w1 + 2) + "┬" + "─" * (w2 + 2) + "┐"
    mid = "├" + "─" * (w1 + 2) + "┼" + "─" * (w2 + 2) + "┤"
    bot = "└" + "─" * (w1 + 2) + "┴" + "─" * (w2 + 2) + "┘"

    def line(a, b):
        return ("│ " + a + " " * (w1 - _w(a) + 1)
                + "│ " + b + " " * (w2 - _w(b) + 1) + "│")

    out = [top, line(*headers), mid] + [line(a, b) for a, b in rows] + [bot]
    return out


def render_text(rep):
    L = []
    L.append("=" * 48)
    L.append("号码标记查询结果（九大平台）")
    L.append("=" * 48)
    L.append("查询号码 : %s" % rep["phone"])
    L.append("查询时间 : %s" % rep["queried_at"])
    L.append("平台命中 : %d/%d" % (rep["marked_count"], rep["platform_total"]))

    def mark_text(p):
        if p["marked"] is True:
            t = p["label"]
            if p["count"]:
                t += "（约%s人标记）" % p["count"]
            return t
        if p["marked"] is False:
            return "无标记"
        return "未知(%.30s)" % p["raw"]

    rows = [(p["name"], mark_text(p)) for p in rep["platforms"]]
    L.extend(_table(rows, ("平台", "标记情况")))
    L.append("风险等级 : %s" % rep["risk_level"])
    if rep["risk_keywords"]:
        L.append("判定依据 : 命中关键词「%s」（来源见上表）"
                 % "、".join(rep["risk_keywords"]))
    L.append("接听建议 : %s" % rep["advice"])
    L.append("-" * 48)
    L.append("今日用量 : %d/%d    设备UID: %s…"
             % (rep["used"], rep["limit"], rep["uid"][:8]))
    if rep["respid"]:
        L.append("请求ID   : %s" % rep["respid"])
    return "\n".join(L)


def emit_error(as_json, code, message):
    if as_json:
        print(json.dumps({"ok": False, "error": message}, ensure_ascii=False))
    else:
        print("错误: %s" % message)
    sys.exit(code)


# ---------------- 命令入口 ----------------

def cmd_query(phone_raw, as_json):
    try:
        phone = normalize_phone(phone_raw)
    except ValueError as e:
        emit_error(as_json, 1, str(e))

    state = load_state()
    limit = effective_limit(state)
    if int(state["used"]) >= limit:
        emit_error(as_json, 2, "今日免费额度已用完（%d/%d），明天自动重置；"
                   "限额可由部署方通过 --set-limit 或环境变量 %s 调整"
                   % (state["used"], limit, ENV_DAILY_LIMIT))

    api = os.environ.get(ENV_API_URL, "").strip() or API_URL
    if "REPLACE_WITH_YOUR_DOMAIN" in api:
        emit_error(as_json, 3, "接口域名未配置：请先编辑 scripts/query.py 顶部的 "
                   "API_URL 占位符（或设置环境变量 %s）" % ENV_API_URL)

    url = "%s?%s" % (api, urllib.parse.urlencode({"sj": phone, "uid": state["uid"]}))
    try:
        data = http_get_json(url)
    except RuntimeError as e:
        emit_error(as_json, 3, str(e))
    if not isinstance(data, dict) or "phone" not in data:
        emit_error(as_json, 3, "接口返回格式异常: %.200s"
                   % json.dumps(data, ensure_ascii=False))

    state["used"] = int(state.get("used", 0)) + 1
    save_state(state)

    rep = build_report(phone, data, state, limit)
    rep["ok"] = True
    print(json.dumps(rep, ensure_ascii=False, indent=2) if as_json else render_text(rep))


def cmd_status(as_json):
    state = load_state()
    limit = effective_limit(state)
    save_state(state)
    payload = {
        "ok": True,
        "uid": state["uid"],
        "date": state["date"],
        "used": int(state["used"]),
        "limit": limit,
        "state_file": str(STATE_FILE),
        "api_url": os.environ.get(ENV_API_URL, "").strip() or API_URL,
    }
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("设备 UID   : %s" % payload["uid"])
        print("今日用量   : %d/%d（%s）" % (payload["used"], limit, payload["date"]))
        print("每日限额   : %d（--set-limit N 可修改）" % limit)
        print("状态文件   : %s" % payload["state_file"])
        print("接口地址   : %s" % payload["api_url"])


def cmd_set_limit(n):
    if n <= 0:
        print("错误: 次数必须为正整数")
        sys.exit(1)
    state = load_state()
    state["daily_limit"] = n
    save_state(state)
    print("已设置每天免费查询次数 = %d（配置文件: %s）" % (n, STATE_FILE))


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(
        prog="query.py", description="号码标记一键查询（九大平台聚合）")
    ap.add_argument("phone", nargs="?", help="手机号或带区号固话，如 13800138000 / 031168179468")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出结果")
    ap.add_argument("--status", action="store_true", help="查看设备 UID、今日用量与限额")
    ap.add_argument("--set-limit", type=int, metavar="N", help="设置每天免费查询次数")
    args = ap.parse_args(argv)

    if args.set_limit is not None:
        return cmd_set_limit(args.set_limit)
    if args.status:
        return cmd_status(args.json)
    if not args.phone:
        ap.print_usage()
        print("错误: 请提供要查询的号码，或使用 --status / --set-limit")
        sys.exit(1)
    return cmd_query(args.phone, args.json)


if __name__ == "__main__":
    main()
