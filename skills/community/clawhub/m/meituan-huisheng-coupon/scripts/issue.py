#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
if hasattr(sys.stdout, 'buffer') and sys.stdout.encoding.lower().replace('-','') != 'utf8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if hasattr(sys.stderr, 'buffer') and sys.stderr.encoding.lower().replace('-','') != 'utf8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
"""
私域领券工具（huisheng-coupon-tool）- 发券脚本
接口：POST https://media.meituan.com/fulishemini/couponActivity/sendCouponByAi
用法：python issue.py --token <user_token>
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'vendor'))
import cliguard

# ── 常量 ──────────────────────────────────────────────────────────────
# 发券接口的域名
BASE_URL   = "https://media.meituan.com"
# 发券接口路径，完整地址 = BASE_URL + ISSUE_PATH
ISSUE_PATH = "/fulishemini/couponActivity/sendCouponByAi"

# config.json 路径（scripts/ 的上级目录，即 Skill 根目录）
_CONFIG_FILE = Path(__file__).parent / "config.json"


def load_config() -> dict:
    """读取 Skill 配置文件 config.json，文件不存在或解析失败时返回空字典"""
    if _CONFIG_FILE.exists():
        try:
            with open(_CONFIG_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def fen_to_yuan(fen) -> str:
    """
    将金额从「分」转换为「元」，格式化为字符串。
    整数去掉小数点（1000分→"10"），非整数保留1位小数（1050分→"10.5"）。
    """
    if not fen:
        return "0"
    yuan = int(fen) / 100
    return str(int(yuan)) if yuan == int(yuan) else f"{yuan:.1f}"



def format_timestamp_ms(ts_ms) -> str:
    """
    将毫秒级时间戳转换为可读日期字符串（格式：YYYY-MM-DD，天维度）。
    传入 None/空时返回 "-"，转换异常时返回原始值字符串（兜底）。
    """
    if not ts_ms:
        return "-"
    try:
        return datetime.fromtimestamp(int(ts_ms) / 1000).strftime("%Y-%m-%d")
    except Exception:
        return str(ts_ms)



def format_coupon(c: dict) -> dict:
    """格式化单张券信息，只保留展示所需字段"""
    price_limit = c.get("priceLimit")
    coupon_value = c.get("couponValue", 0)
    if price_limit and price_limit > 0:
        discount_info = f"满{fen_to_yuan(price_limit)}元减{fen_to_yuan(coupon_value)}元"
    else:
        discount_info = ""
    # 有效期：couponStartTime + couponEndTime 都有值才组合，转为天维度
    start = c.get("couponStartTime")
    end = c.get("couponEndTime")
    valid_period = ""
    if start and end:
        valid_period = f"{format_timestamp_ms(start)} 至 {format_timestamp_ms(end)}"
    return {
        "name": c.get("couponName", ""),
        "discount_info": discount_info,
        "valid_period": valid_period,
        "priceLimit": price_limit,
        "couponValue": coupon_value,
        "tabName": c.get("tabName", ""),
    }


# ── 日志路径 ──────────────────────────────────────────────────────────
import tempfile
_LOG_FILE = Path(tempfile.gettempdir()) / "huisheng" / "huisheng_issue.log"


def _get_device_token() -> str:
    """从 auth_tokens.json 读取 device_token，读取失败返回空字符串"""
    try:
        env_path = os.environ.get("XIAOMEI_AUTH_FILE")
        if env_path:
            token_file = Path(env_path)
        else:
            token_file = Path.home() / ".xiaomei-workspace" / "auth_tokens.json"
        with open(token_file, encoding="utf-8") as f:
            return json.load(f).get("device_token", "")
    except Exception:
        return ""


def _xor_encrypt(data: str, ai_scene: str) -> str:
    """XOR 加密，返回带 flag 前缀的 hex 字符串。
    前缀 '1:' = key 用 sha256(device_token + aiScene)
    前缀 '0:' = 降级，key 用 sha256(aiScene)
    flag 保证解密时能还原正确的 key，不依赖运行时环境。
    """
    import hashlib
    device_token = _get_device_token()
    if device_token:
        seed = device_token + ai_scene
        flag = "1"
    else:
        seed = ai_scene
        flag = "0"
    key_bytes = hashlib.sha256(seed.encode()).digest()
    data_bytes = data.encode("utf-8")
    result = bytes(b ^ key_bytes[i % 32] for i, b in enumerate(data_bytes))
    return flag + ":" + result.hex()


def write_log(entry: dict, ai_scene: str = ""):
    """将单次执行记录加密后追加写入日志文件，每条一行；任何异常静默跳过"""
    try:
        _LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        raw = json.dumps(entry, ensure_ascii=False)
        encrypted = _xor_encrypt(raw, ai_scene) if ai_scene else raw
        with open(_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(encrypted + "\n")
    except Exception:
        pass  # 日志写失败不影响主流程


# ── 展示结果构建（独立方法，不需要时可整体删除） ──────────────────────────
# 删除方式：删除 _build_count_str、_build_display_coupons、build_display_result
# 三个函数，以及 main() 中 result 字典里的 count_str 和 display_coupons 两行赋值即可。

_TAB_ORDER = ["外卖", "美食团购", "美团闪购", "休闲娱乐", "生活服务", "丽人医疗", "更多福利"]
_TAB_DISPLAY = {"更多福利": "其他"}
_SLOT_PLAN_BASE = [("外卖", 2), ("美食团购", 1), ("美团闪购", 1),
                   ("休闲娱乐", 1), ("生活服务", 1), ("丽人医疗", 1)]


def _build_count_str(coupons: list) -> str:
    """
    按 TAB_ORDER 对券列表分组计数，应用 TAB_DISPLAY 重命名，
    生成形如「美食团购优惠券7张、休闲娱乐优惠券10张、其他优惠券2张」的字符串。
    统计数量严格来自原始券列表，与展示表格无关。
    """
    tab_count: dict = {}
    for c in coupons:
        tab = c.get("tabName", "")
        tab_count[tab] = tab_count.get(tab, 0) + 1

    unknown_tabs = [t for t in tab_count if t not in _TAB_ORDER]
    final_order = _TAB_ORDER[:6] + unknown_tabs + _TAB_ORDER[6:]

    parts = []
    for tab in final_order:
        if tab not in tab_count:
            continue
        display_name = _TAB_DISPLAY.get(tab, tab)
        parts.append(f"{display_name}优惠券{tab_count[tab]}张")
    return "、".join(parts)


def _build_display_coupons(coupons: list) -> list:
    """
    按 SLOT_PLAN 分槽 + fallback 补位，最多取 8 张用于展示。
    排序规则：无门槛券优先，有门槛券按补贴率（couponValue/priceLimit）降序。
    返回格式化后的券列表，字段与 format_coupon() 输出一致。
    """
    def sort_key(c):
        pl = c.get("priceLimit")
        if not pl:
            return (0, 0)
        return (1, -(c.get("couponValue", 0) / pl))

    # 按 tabName 分组并排序
    groups: dict = {}
    for c in coupons:
        tab = c.get("tabName", "")
        groups.setdefault(tab, []).append(c)
    for tab in groups:
        groups[tab].sort(key=sort_key)

    unknown_tabs = [t for t in groups if t not in _TAB_ORDER]
    slot_plan = _SLOT_PLAN_BASE + [(t, 1) for t in unknown_tabs] + [("更多福利", 1)]

    used: dict = {}
    slots: list = []

    # 第一轮：按 SLOT_PLAN 分配
    for tab, quota in slot_plan:
        if len(slots) >= 8:
            break
        taken = 0
        for c in groups.get(tab, []):
            if taken >= quota or len(slots) >= 8:
                break
            slots.append(c)
            used[tab] = used.get(tab, 0) + 1
            taken += 1

    # 第二轮：fallback 补位至 8 张
    fallback_order = ["外卖", "美食团购", "美团闪购", "休闲娱乐", "生活服务", "丽人医疗"] \
                     + unknown_tabs + ["更多福利"]
    while len(slots) < 8:
        filled = False
        for tab in fallback_order:
            remaining = groups.get(tab, [])[used.get(tab, 0):]
            if remaining:
                slots.append(remaining[0])
                used[tab] = used.get(tab, 0) + 1
                filled = True
                break
        if not filled:
            break

    return slots


def build_display_result(coupons: list) -> dict:
    """
    对外入口：接收格式化后的券列表，返回 count_str 和 display_coupons。
    在 main() 的成功分支中调用，结果直接合并进输出 JSON。
    """
    return {
        "count_str": _build_count_str(coupons),
        "display_coupons": _build_display_coupons(coupons),
    }

# ── 展示结果构建 END ───────────────────────────────────────────────────


def main():
    # 定义命令行入口，必须传入 --token 参数（用户登录后的 user_token）
    parser = argparse.ArgumentParser(description="私域领券 发券脚本")
    parser.add_argument("--token", required=True, help="用户 user_token")
    args = parser.parse_args()

    import httpx

    # ── 构造请求体 ────────────────────────────────────────────────────
    config = load_config()
    body = {
        "token": args.token,
        "aiScene": config.get("aiScene", ""),
        "version":2
    }

    ai_scene = config.get("aiScene", "")
    log_entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "request": {
            "url": BASE_URL + ISSUE_PATH,
            "aiScene": ai_scene,
            "token_masked": args.token[:8] + "****" if args.token else "",
        }
    }

    # ── 发起 HTTP 请求 ────────────────────────────────────────────────
    try:
        resp = httpx.post(
            BASE_URL + ISSUE_PATH,
            json=body,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                "X-Requested-With": "XMLHttpRequest",
            },
            timeout=15,
            verify=True,
            trust_env=False
        )
        log_entry["response"] = {"http_status": resp.status_code, "body": resp.text[:500]}
        resp_data = resp.json()
    except httpx.TimeoutException:
        log_entry["response"] = {"error": "TIMEOUT"}
        write_log(log_entry, config.get("aiScene", ""))
        print(json.dumps({
            "success": False,
            "error": "TIMEOUT",
            "message": "请求超时，请稍后重试"
        }, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        log_entry["response"] = {"error": "NETWORK_ERROR", "detail": str(e)}
        write_log(log_entry, config.get("aiScene", ""))
        print(json.dumps({
            "success": False,
            "error": "NETWORK_ERROR",
            "message": f"网络异常：{str(e)}"
        }, ensure_ascii=False))
        sys.exit(1)

    # ── 解析响应 ──────────────────────────────────────────────────────
    code = resp_data.get("code")
    msg  = resp_data.get("msg", "")
    data = resp_data.get("data") or {}

    if code == 200:
        # ── 领券成功 ──────────────────────────────────────────────────
        coupon_list = data.get("couponList", [])
        formatted_coupons = [format_coupon(c) for c in coupon_list]
        display = build_display_result(formatted_coupons)
        result = {
            "success": True,
            "code": 200,
            "coupon_count": len(formatted_coupons),
            "coupons": formatted_coupons,
            "count_str": display["count_str"],           # 新增：分类计数字符串
            "display_coupons": display["display_coupons"], # 新增：筛选后的展示券列表
            "activity_name": data.get("activityName", ""),
            "activity_link": data.get("activityLink", ""),
        }
        log_entry["result"] = {"success": True, "code": 200, "coupon_count": len(formatted_coupons)}
        write_log(log_entry, config.get("aiScene", ""))
        print(json.dumps(result, ensure_ascii=False))

    elif code == 1014:
        # ── 今日已领取，仍返回活动信息 ───────────────────────────────
        result = {
            "success": False,
            "code": 1014,
            "error": "ALREADY_RECEIVED",
            "message": "您今天已经领取过了，每天只能领取一次，明天再来哦～",
            "activity_name": data.get("activityName", ""),
            "activity_link": data.get("activityLink", ""),
        }
        log_entry["result"] = {"success": False, "code": 1014, "error": "ALREADY_RECEIVED"}
        write_log(log_entry, config.get("aiScene", ""))
        print(json.dumps(result, ensure_ascii=False))

    elif code == 401:
        result = {"success": False, "code": 401, "error": "RE_LOGIN", "message": "登录已过期，请重新登录"}
        log_entry["result"] = {"success": False, "code": 401, "error": "RE_LOGIN"}
        write_log(log_entry, config.get("aiScene", ""))
        print(json.dumps(result, ensure_ascii=False))

    elif code in (509, 50200):
        result = {"success": False, "code": code, "error": "RATE_LIMIT", "message": "请求过于频繁，请稍后重试"}
        log_entry["result"] = {"success": False, "code": code, "error": "RATE_LIMIT"}
        write_log(log_entry, config.get("aiScene", ""))
        print(json.dumps(result, ensure_ascii=False))

    elif code == 9999:
        result = {"success": False, "code": 9999, "error": "SYSTEM_ERROR", "message": "系统异常，请稍后重试"}
        log_entry["result"] = {"success": False, "code": 9999, "error": "SYSTEM_ERROR"}
        write_log(log_entry, config.get("aiScene", ""))
        print(json.dumps(result, ensure_ascii=False))

    else:
        result = {"success": False, "code": code, "error": "UNKNOWN_ERROR", "message": f"未知错误（code={code}，msg={msg}）"}
        log_entry["result"] = {"success": False, "code": code, "error": "UNKNOWN_ERROR"}
        write_log(log_entry, config.get("aiScene", ""))
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
