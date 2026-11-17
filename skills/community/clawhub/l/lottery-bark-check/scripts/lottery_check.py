#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lottery-bark-check · 中国彩票开奖核对与 Bark 推送（通用版）

流程：抓取中彩网（双色球）/ 500 网（大乐透）最新真实开奖
      → 与你的守号比对 → 判定奖级与金额 → 按定稿版式生成报告
      → 仅通过 Bark 推送到手机（group 固定「彩票」）。

零依赖：Python 3 标准库 + curl。

快速开始：
  python3 lottery_check.py --init                 # 生成 ~/.lottery/config.json 示例
  export BARK_DEVICE_KEY='你的device_key'
  python3 lottery_check.py --ssq "03 04 11 12 13 28 + 01" --dry-run
  python3 lottery_check.py --ssq "03 04 11 12 13 28 + 01"

安全约定：
  * device_key 只从环境变量 BARK_DEVICE_KEY 或配置文件读取，日志/预览一律脱敏；
  * 只走 Bark，不调用任何其它推送通道。
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import time
import urllib.request

# ===== 固定配置（版式与通道已定稿，勿改）=====
BARK_URL = "https://api.day.app/push"
LINK = "https://bark.day.app"
WJ = "\u2060"
DEFAULT_GROUP = "彩票"
DEFAULT_LEVEL = "timeSensitive"
DEFAULT_SOUND = "bell"
WEEKDAY_CN = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
CONFIG_PATH = os.path.expanduser("~/.lottery/config.json")

TIER = {1: "一等奖", 2: "二等奖", 3: "三等奖", 4: "四等奖", 5: "五等奖", 6: "六等奖"}
DLT_FIXED = {3: 10000, 4: 3000, 5: 300, 6: 200}
SSQ_DRAW_DAYS = {1, 3, 6}      # 周二 / 周四 / 周日
DLT_DRAW_DAYS = {0, 2, 5}      # 周一 / 周三 / 周六

EXAMPLE_CONFIG = {
    "bark_device_key": "在此填写你的 Bark device_key（或用环境变量 BARK_DEVICE_KEY）",
    "group": "彩票",
    "level": "timeSensitive",
    "sound": "bell",
    "notes": {
        "ssq": [{"red": [3, 4, 11, 12, 13, 28], "blue": [1]}],
        "dlt": [{"front": [3, 4, 11, 13, 28], "back": [1, 12]}],
    },
}


def z2(n):
    return str(int(n)).zfill(2)


# ===== 数据抓取（官方源）=====
def fetch_url(url, timeout=15, retries=3):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    last = None
    for _ in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "ignore")
        except Exception as e:            # noqa: BLE001
            last = e
            time.sleep(2)
    raise last


def fetch_ssq():
    url = ("https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/"
           "findDrawNotice?name=ssq&issueCount=1")
    d = json.loads(fetch_url(url))
    r = d["result"][0]
    m = re.search(r"(\d{4}-\d{2}-\d{2})", r["date"])
    return {"code": r["code"], "date": m.group(1) if m else "",
            "red": [int(x) for x in r["red"].split(",")],
            "blue": int(r["blue"]),
            "prizegrades": r.get("prizegrades", [])}


def fetch_dlt():
    url = ("https://datachart.500.com/dlt/history/newinc/history.php"
           "?start=26000&end=29999")
    html = fetch_url(url)
    m = re.search(r'id="tdata">(.*?)</tbody>', html, re.S)
    if not m:
        raise ValueError("大乐透数据解析失败（tdata 为空）")
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", m.group(1), re.S)
    if not rows:
        raise ValueError("大乐透数据解析失败（无行）")
    cells = [re.sub(r"<[^>]*>", "", c).strip()
             for c in re.findall(r"<td[^>]*>(.*?)</td>", rows[0], re.S)]
    return {"code": cells[1],
            "front": [int(cells[2]), int(cells[3]), int(cells[4]), int(cells[5]), int(cells[6])],
            "back": [int(cells[7]), int(cells[8])],
            "date": cells[-1]}


# ===== 奖级判定 =====
def ssq_tier(mr, mb):
    if mr == 6 and mb == 1: return 1
    if mr == 6 and mb == 0: return 2
    if mr == 5 and mb == 1: return 3
    if (mr == 5 and mb == 0) or (mr == 4 and mb == 1): return 4
    if (mr == 4 and mb == 0) or (mr == 3 and mb == 1): return 5
    if mr in (0, 1, 2) and mb == 1: return 6
    return 0


def dlt_tier(mf, mb):
    if mf == 5 and mb == 2: return 1
    if mf == 5 and mb == 1: return 2
    if (mf == 5 and mb == 0) or (mf == 4 and mb == 2): return 3
    if (mf == 4 and mb == 1) or (mf == 3 and mb == 2): return 4
    if (mf == 4 and mb == 0) or (mf == 3 and mb == 1) or (mf == 2 and mb == 2): return 5
    if mf in (0, 1, 2, 3) and mb == 2: return 6
    return 0


def ssq_amount(tier, prizegrades):
    for g in prizegrades:
        if int(g.get("type", 0)) == tier:
            try:
                return int(str(g.get("typemoney", "0")).replace(",", ""))
            except ValueError:
                return 0
    return 0


# ===== 版式与配色（定稿，勿改）=====
def blue(n):
    """蓝色号码：链接写法（Bark 中唯一可用颜色），字体与黑字一致，自带下划线。"""
    return f"[{z2(n)}]({LINK})"


def blue_bold(s):
    return f"**[{s}]({LINK})**"


def fmt_row(groups, draw_groups, all_blue):
    """开奖行全蓝；我的行仅命中蓝。号码间插 U+2060 打断 iOS 电话号自动染蓝。"""
    segs = []
    for nums, dg in zip(groups, draw_groups):
        parts = []
        for n in nums:
            hit = all_blue or (n in dg)
            parts.append(blue(n) if hit else z2(n))
        segs.append((WJ + " ").join(parts))
    return " + ".join(segs)


def validate_layout(md):
    """排版锁：结构偏离定稿模板即拒绝推送。"""
    secs = md.split("\n\n")
    ok = len(secs) >= 4 and secs[0].startswith("开奖 ") and secs[-1].startswith("本期总计 ¥")
    if ok:
        mine = re.compile(r"^(?:[①②③④⑤⑥⑦⑧⑨⑩]\s*)?我的 ")
        mid = secs[1:-1]
        ok = len(mid) % 2 == 0 and all(
            mine.match(mid[i]) and mid[i + 1].startswith("合计 ")
            for i in range(0, len(mid), 2))
    if not ok:
        raise RuntimeError("排版校验失败：正文结构偏离定稿模板，已阻止推送。\n" + md)


def build_report(kind, draw, target_date, notes):
    tag = f"{target_date.month}/{target_date.day} {WEEKDAY_CN[target_date.weekday()]}"
    multi = len(notes) > 1
    blocks, total, win, max_tier, floating = [], 0, 0, 0, False

    if kind == "ssq":
        kind_cn = "双色球"
        draw_groups = [draw["red"], [draw["blue"]]]
    else:
        kind_cn = "大乐透"
        draw_groups = [draw["front"], draw["back"]]

    for i, note in enumerate(notes):
        if kind == "ssq":
            my_groups = [note["red"], note["blue"]]
            m1 = sum(1 for n in my_groups[0] if n in draw["red"])
            m2 = 1 if my_groups[1][0] == draw["blue"] else 0
            tier = ssq_tier(m1, m2)
        else:
            my_groups = [note["front"], note["back"]]
            m1 = sum(1 for n in my_groups[0] if n in draw["front"])
            m2 = sum(1 for n in my_groups[1] if n in draw["back"])
            tier = dlt_tier(m1, m2)

        if tier > 0:
            win += 1
            max_tier = max(max_tier, tier)
            if kind == "ssq":
                amt = ssq_amount(tier, draw["prizegrades"])
                total += amt
                amt_s = f"¥{amt:,}"
            elif tier in (1, 2):
                floating = True
                amt_s = "浮动奖（以公告为准）"
            else:
                amt = DLT_FIXED.get(tier, 0)
                total += amt
                amt_s = f"¥{amt:,}"
            result = f"合计 {m1}+{m2} → {blue_bold('中奖')} {TIER[tier]} {blue_bold(amt_s)}"
        else:
            result = f"合计 {m1}+{m2} → 未中奖"

        head = (("①②③④⑤⑥⑦⑧⑨⑩"[i] + " ") if multi else "")
        blocks.append(f"{head}我的 {fmt_row(my_groups, draw_groups, all_blue=False)}")
        blocks.append(result)

    draw_row = fmt_row(draw_groups, draw_groups, all_blue=True)
    md = (f"开奖 {draw_row}\n\n" + "\n\n".join(blocks) +
          f"\n\n本期总计 ¥{total:,}")
    validate_layout(md)

    subtitle = "中奖" if win > 0 else "未中奖"
    return {"title": f"彩票 {tag} · {kind_cn}", "subtitle": subtitle,
            "markdown": md, "kind_cn": kind_cn, "total": total, "win": win}


# ===== Bark 推送（唯一通道）=====
def push_bark(cfg, *, title, subtitle=None, body=None, markdown=None, dry_run=False):
    payload = {"device_key": cfg["bark_device_key"], "title": title,
               "group": cfg.get("group", DEFAULT_GROUP),
               "level": cfg.get("level", DEFAULT_LEVEL),
               "sound": cfg.get("sound", DEFAULT_SOUND)}
    if subtitle is not None:
        payload["subtitle"] = subtitle
    if markdown is not None:
        payload["markdown"] = markdown
    else:
        payload["body"] = body

    if dry_run:
        safe = dict(payload)
        safe["device_key"] = "***REDACTED***" if cfg["bark_device_key"] else "(未设置)"
        print("[dry-run] payload：")
        print(json.dumps(safe, ensure_ascii=False, indent=2))
        return "DRY_RUN"

    data = json.dumps(payload, ensure_ascii=False)
    try:
        p = subprocess.run(["curl", "-sS", "--max-time", "20", "-X", "POST",
                            BARK_URL, "-H", "Content-Type: application/json",
                            "-d", data], capture_output=True, text=True, timeout=30)
        out = p.stdout.strip()
        try:
            return json.loads(out).get("code")
        except Exception:                 # noqa: BLE001
            return out
    except Exception as e:                # noqa: BLE001
        return f"ERR:{e}"


# ===== 配置 =====
def parse_ssq(text):
    """'03 04 11 12 13 28 + 01' 或 '... ; ...'（多注分号分隔）"""
    notes = []
    for chunk in re.split(r"[;；]", text):
        chunk = chunk.strip()
        if not chunk:
            continue
        red_s, _, blue_s = chunk.partition("+")
        red = [int(x) for x in re.findall(r"\d{1,2}", red_s)]
        bl = [int(x) for x in re.findall(r"\d{1,2}", blue_s)]
        if len(red) != 6 or len(bl) != 1:
            raise ValueError(f"双色球守号格式应为 6 红 + 1 蓝：{chunk}")
        notes.append({"red": red, "blue": bl})
    return notes


def parse_dlt(text):
    """'03 04 11 13 28 + 01 12' 或 '... ; ...'"""
    notes = []
    for chunk in re.split(r"[;；]", text):
        chunk = chunk.strip()
        if not chunk:
            continue
        f_s, _, b_s = chunk.partition("+")
        front = [int(x) for x in re.findall(r"\d{1,2}", f_s)]
        back = [int(x) for x in re.findall(r"\d{1,2}", b_s)]
        if len(front) != 5 or len(back) != 2:
            raise ValueError(f"大乐透守号格式应为 5 前区 + 2 后区：{chunk}")
        notes.append({"front": front, "back": back})
    return notes


def load_config(args):
    cfg = {"group": DEFAULT_GROUP, "level": DEFAULT_LEVEL, "sound": DEFAULT_SOUND,
           "notes": {"ssq": [], "dlt": []}}
    path = args.config or CONFIG_PATH
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            cfg.update({k: v for k, v in data.items() if k != "notes"})
            for k in ("ssq", "dlt"):
                cfg["notes"][k] = data.get("notes", {}).get(k, []) or []
        except Exception as e:            # noqa: BLE001
            print(f"STATUS: WARN 配置文件读取失败（{e}），改用命令行/环境变量")
    if args.ssq:
        cfg["notes"]["ssq"] = parse_ssq(args.ssq)
    if args.dlt:
        cfg["notes"]["dlt"] = parse_dlt(args.dlt)
    key = (os.environ.get("BARK_DEVICE_KEY", "") or cfg.get("bark_device_key", "")).strip()
    if key.startswith("在此填写"):
        key = ""
    cfg["bark_device_key"] = key
    return cfg


def init_config(path):
    if os.path.exists(path):
        print(f"配置文件已存在，未覆盖：{path}")
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(EXAMPLE_CONFIG, f, ensure_ascii=False, indent=2)
    print(f"已生成示例配置：{path}\n请填入 device_key 与守号后运行。")


def main():
    ap = argparse.ArgumentParser(description="中国彩票开奖核对与 Bark 推送")
    ap.add_argument("--config", help=f"配置文件路径（默认 {CONFIG_PATH}）")
    ap.add_argument("--ssq", help='双色球守号，如 "03 04 11 12 13 28 + 01"，多注用 ; 分隔')
    ap.add_argument("--dlt", help='大乐透守号，如 "03 04 11 13 28 + 01 12"，多注用 ; 分隔')
    ap.add_argument("--dry-run", action="store_true", help="只预览 payload，不推送")
    ap.add_argument("--date", help="复测指定日期 YYYY-MM-DD")
    ap.add_argument("--init", action="store_true", help="生成示例配置文件")
    args = ap.parse_args()

    if args.init:
        init_config(args.config or CONFIG_PATH)
        return

    cfg = load_config(args)
    if not cfg["bark_device_key"] and not args.dry_run:
        print("STATUS: ERROR 未设置 Bark device_key（环境变量 BARK_DEVICE_KEY 或配置文件），取消推送")
        sys.exit(1)

    today = datetime.date.fromisoformat(args.date) if args.date else datetime.date.today()
    tag = f"{today.month}/{today.day} {WEEKDAY_CN[today.weekday()]}"
    print(f"云时间 {today.isoformat()}（{tag}）")

    if not cfg["notes"]["ssq"] and not cfg["notes"]["dlt"]:
        print("STATUS: ERROR 没有守号，请用 --ssq/--dlt 指定或先运行 --init")
        sys.exit(1)

    try:
        ssq = fetch_ssq()
        dlt = fetch_dlt()
    except Exception as e:                # noqa: BLE001
        print(f"STATUS: ERROR 抓取开奖数据失败：{e}")
        sys.exit(1)

    ssq_drew = (ssq["date"] == today.isoformat())
    dlt_drew = (dlt["date"] == today.isoformat())
    print(f"双色球 最新期 {ssq['code']} 日期 {ssq['date']} 今日开奖={ssq_drew}")
    print(f"大乐透 最新期 {dlt['code']} 日期 {dlt['date']} 今日开奖={dlt_drew}")

    draw_day = (today.weekday() in SSQ_DRAW_DAYS) or (today.weekday() in DLT_DRAW_DAYS)
    wait = 0 if args.dry_run else 90
    for attempt in range(3):
        if (today.weekday() in SSQ_DRAW_DAYS) and not ssq_drew:
            try:
                ssq = fetch_ssq(); ssq_drew = (ssq["date"] == today.isoformat())
            except Exception:             # noqa: BLE001
                pass
        if (today.weekday() in DLT_DRAW_DAYS) and not dlt_drew:
            try:
                dlt = fetch_dlt(); dlt_drew = (dlt["date"] == today.isoformat())
            except Exception:             # noqa: BLE001
                pass
        if ssq_drew or dlt_drew:
            break
        if attempt < 2 and draw_day and wait:
            time.sleep(wait)

    if ssq_drew and cfg["notes"]["ssq"]:
        rep = build_report("ssq", ssq, today, cfg["notes"]["ssq"])
        code = push_bark(cfg, title=rep["title"], subtitle=rep["subtitle"],
                         markdown=rep["markdown"], dry_run=args.dry_run)
        print(f"STATUS: HAS_RESULT {rep['kind_cn']} 推送 code={code}")
        print("--- markdown ---")
        print(rep["markdown"])
        return
    if dlt_drew and cfg["notes"]["dlt"]:
        rep = build_report("dlt", dlt, today, cfg["notes"]["dlt"])
        code = push_bark(cfg, title=rep["title"], subtitle=rep["subtitle"],
                         markdown=rep["markdown"], dry_run=args.dry_run)
        print(f"STATUS: HAS_RESULT {rep['kind_cn']} 推送 code={code}")
        print("--- markdown ---")
        print(rep["markdown"])
        return

    if today.weekday() == 4:
        code = push_bark(cfg, title=f"彩票 {tag} · 周五不开奖", body="周五不开奖",
                         dry_run=args.dry_run)
        print(f"STATUS: NO_NEW_DRAW(周五) 推送 code={code}")
        return

    code = push_bark(cfg, title=f"彩票 {tag} · 开奖数据暂未更新",
                     body="今日为开奖日，但官方开奖数据暂未发布，未能核对。可稍后手动重查，不会漏期。",
                     dry_run=args.dry_run)
    print(f"STATUS: NO_NEW_DRAW(数据未更新) 推送 code={code}")


if __name__ == "__main__":
    main()
