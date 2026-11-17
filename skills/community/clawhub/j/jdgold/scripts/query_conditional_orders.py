#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# ⚠️ 本文件是「京东黄金 (jdgold)」JoyCode Skill 的组成脚本。
# 执行任何脚本前，必须先阅读 Skill 根目录下的 SKILL.md，
# 严格遵循其中的执行契约、安全脱敏铁律与回复规范，
# 请勿脱离 SKILL.md 指引单独运行本脚本。
# ============================================================
"""黄金条件单查询：通过 cf-gold-ai BFF /api/v1/conditional 调用。

  - 列表：POST /api/v1/conditional/list   { accessToken, bankCode, statusList, ... }
  - 详情：POST /api/v1/conditional/detail { accessToken, bankCode, conditionalUuid, ... }

后端按 ``bankCode`` 路由到对应银行的条件单服务（民生/兴业/中信/浙商）。

触发词："条件单" / "限价买入" / "限价卖出" / "止盈止损" / "自动买卖" / "设定金价自动买卖" / "到价提醒" / "我的条件单" / "查看条件单"
"""
import argparse
import json
import sys
import time
import urllib.error
from typing import Optional, Dict

import bff_client
import jos

# 银行 → productSku 映射（保留给本地展示使用，BFF 内部已封装）
BANK_SKU_MAP = {
    "CMBC": "",
    "CIB": "CIB-JCJ0",
    "CITIC": "CNCB-JCJ",
    "CZB": "CZB-JCJ",
}

# ── 条件单状态映射 ──────────────────────────────────────────────────
STATUS_MAP = {
    "1": "生效中",
    "2": "已触发",
    "3": "已失效",
    "4": "已取消",
    "5": "已完成",
}

# ── 条件单类型映射 ──────────────────────────────────────────────────
TRADE_TYPE_MAP = {
    "1": "限价买入",
    "2": "限价卖出",
    "3": "止盈",
    "4": "止损",
    "5": "止盈止损",
}

# ── 银行名称 ──────────────────────────────────────────────────────
BANK_CONFIG = {
    "CMBC": {"name": "民生银行"},
    "CIB": {"name": "兴业银行"},
    "CITIC": {"name": "中信银行"},
    "CZB": {"name": "浙商银行"},
}


# ── 底层 BFF 调用 ──────────────────────────────────────────────────


def _get_jrid() -> str:
    """获取加密 pin 作为 jrid 参数。BFF 未提供时可返回空字符串，由后端注入。"""
    pin_info = jos.get_session_pin()
    if isinstance(pin_info, tuple):
        return pin_info[0] or ""
    return pin_info or ""


def _call_cond_list(bank_code: str, status_list, page_index: int, page_size: int,
                    start_time: int, end_time: int, product_sku: str = "") -> Optional[dict]:
    """统一调用 BFF 条件单列表接口，返回业务 response（不同银行结构不一致）。"""
    access_token = jos._valid_access_token()
    body = {
        "accessToken": access_token,
        "bankCode": bank_code,
        "jrid": _get_jrid() if bank_code != "CMBC" else "",
        "statusList": status_list or ["1"],
        "pageIndex": page_index,
        "pageSize": page_size,
        "startTime": start_time,
        "endTime": end_time,
    }
    if product_sku:
        body["productSku"] = product_sku
    result = bff_client.post_json(bff_client.PATH_CONDITIONAL_LIST, body)
    if not result:
        return None
    return result.get("response")


def _call_cond_detail(bank_code: str, conditional_uuid: str) -> Optional[dict]:
    """统一调用 BFF 条件单详情接口。"""
    access_token = jos._valid_access_token()
    body = {
        "accessToken": access_token,
        "bankCode": bank_code,
        "conditionalUuid": conditional_uuid,
        "jrid": _get_jrid() if bank_code != "CMBC" else "",
    }
    result = bff_client.post_json(bff_client.PATH_CONDITIONAL_DETAIL, body)
    if not result:
        return None
    return result.get("response")


# ── 条件单列表查询 ──────────────────────────────────────────────────


def _default_time_window(start_time, end_time):
    # 注意：BFF 后端按【毫秒级】时间戳解析 startTime/endTime。
    # 若传秒级(10位)会被当成毫秒，落到 1970 年，导致条件单查不到。
    # 条件单是"等待触发"的未来订单，endTime 需向未来延伸。
    now_ms = int(time.time() * 1000)
    return (
        start_time if start_time is not None else now_ms - 365 * 86400 * 1000,  # 起点回溯 1 年
        end_time if end_time is not None else now_ms + 365 * 86400 * 1000,      # 终点向未来 1 年
    )


def fetch_cmbc_conditional_list(status_list=None, page_index=1, page_size=10,
                                 start_time=None, end_time=None) -> Optional[dict]:
    s, e = _default_time_window(start_time, end_time)
    return _call_cond_list("CMBC", status_list, page_index, page_size, s, e)


def fetch_std_conditional_list(bank_code, eid="", product_sku="",
                                status_list=None, page_index=1, page_size=10,
                                start_time=None, end_time=None) -> Optional[dict]:
    s, e = _default_time_window(start_time, end_time)
    return _call_cond_list(bank_code, status_list, page_index, page_size, s, e, product_sku)


def fetch_czb_conditional_list(product_sku="", status_list=None,
                                page_index=1, page_size=10,
                                start_time=None, end_time=None) -> Optional[dict]:
    s, e = _default_time_window(start_time, end_time)
    return _call_cond_list("CZB", status_list, page_index, page_size, s, e, product_sku)


def fetch_all_conditional_lists(status_list=None) -> Dict[str, dict]:
    """查询所有银行的条件单列表，返回 {bank_code: result}。
    
    对已开户银行返回条件单数据，对未开户银行返回提示信息。
    """
    results = {}
    
    # 民生
    try:
        r = fetch_cmbc_conditional_list(status_list=status_list)
        results["CMBC"] = r if r else {}
    except RuntimeError as e:
        err_msg = str(e)
        if "未登录" in err_msg:
            raise  # 未登录直接抛出，让上层处理
        results["CMBC"] = {"__error__": err_msg}
    except Exception as e:
        results["CMBC"] = {"__error__": str(e)}

    # 兴业
    try:
        r = fetch_std_conditional_list("CIB", status_list=status_list)
        results["CIB"] = r if r else {}
    except Exception as e:
        results["CIB"] = {"__error__": str(e)}

    # 中信
    try:
        r = fetch_std_conditional_list("CITIC", status_list=status_list)
        results["CITIC"] = r if r else {}
    except Exception as e:
        results["CITIC"] = {"__error__": str(e)}

    # 浙商
    try:
        r = fetch_czb_conditional_list(status_list=status_list)
        results["CZB"] = r if r else {}
    except Exception as e:
        results["CZB"] = {"__error__": str(e)}

    return results


# ── 条件单详情查询 ──────────────────────────────────────────────────


def fetch_conditional_detail(bank_code: str, conditional_uuid: str) -> Optional[dict]:
    """统一条件单详情查询。后端按 ``bankCode`` 路由到对应银行接口。"""
    return _call_cond_detail(bank_code, conditional_uuid)


def fetch_cmbc_conditional_detail(trade_no="", jd_order_id="", pl_order_id="",
                                   trade_type="1") -> Optional[dict]:
    """民生条件单详情（兼容旧签名，uuid 由 ``trade_no`` 或 ``jd_order_id`` 提供）。"""
    return fetch_conditional_detail("CMBC", trade_no or jd_order_id or pl_order_id or "")


def fetch_std_conditional_detail(bank_code, uuid="", trade_type="",
                                  eid="", product_sku="") -> Optional[dict]:
    """兴业/中信条件单详情（兼容旧签名）。"""
    return fetch_conditional_detail(bank_code, uuid)


def fetch_czb_conditional_detail(product_sku="", trade_no="", jd_order_id="",
                                  pl_order_id="", trade_type="1") -> Optional[dict]:
    """浙商条件单详情（兼容旧签名）。"""
    return fetch_conditional_detail("CZB", trade_no or jd_order_id or pl_order_id or "")


# ── 格式化与渲染 ────────────────────────────────────────────────────


_STATUS_EMOJI = {
    "生效中": "🟢", "已触发": "⚡", "已失效": "⚪",
    "已取消": "⚪", "已完成": "✅",
}
_TYPE_EMOJI = {
    "限价买入": "🟢", "限价卖出": "🔴",
    "止盈": "📈", "止损": "📉", "止盈止损": "🎯",
}


def _status_label(code) -> str:
    """条件单状态code → 中文标签（带 emoji）。"""
    label = STATUS_MAP.get(str(code), str(code))
    emoji = _STATUS_EMOJI.get(label, "")
    return f"{emoji} {label}".strip()


def _trade_type_label(code) -> str:
    """条件单类型code → 中文标签（带 emoji）。"""
    label = TRADE_TYPE_MAP.get(str(code), str(code))
    emoji = _TYPE_EMOJI.get(label, "")
    return f"{emoji} {label}".strip()


def _fmt_ts(ts) -> str:
    """毫秒/秒级时间戳 → 可读时间字符串；非法值原样返回。"""
    if ts in (None, "", 0):
        return ""
    try:
        v = int(ts)
    except (ValueError, TypeError):
        return str(ts)
    if v > 10 ** 12:  # 毫秒级
        v = v // 1000
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(v))


_TABLE_HEADER = "| 🏦 银行 | 状态 | 交易类型 | 目标价(元/克) | 克重(克) | 金额(元) | 创建时间 |"
_TABLE_DIVIDER = "| --- | --- | --- | --- | --- | --- | --- |"


def _parse_bank_result(bank_code: str, data):
    """把某家银行的原始返回归一化为四态：error/closed/empty/orders。"""
    if isinstance(data, dict) and "__error__" in data:
        err = str(data.get("__error__", ""))
        if "timeout" in err.lower() or "交易火爆" in err:
            return "error", "银行服务暂不可用（可能网关超时/停用），请稍后重试"
        return "error", f"{err}（接口异常，请稍后重试）"

    if isinstance(data, dict):
        code = data.get("code", "")
        if code and code.startswith("0001"):
            msg = data.get("message", "")
            if "未开户" in msg:
                return "closed", "您未在该银行开户"
            return "closed", msg

        status = data.get("status", "")
        if status == "FAIL":
            err_code = data.get("errorCode", "")
            err_msg = data.get("errorMessage", "")
            if "未开户" in err_msg or err_code == "00010026":
                return "closed", "您未在该银行开户"
            if "交易火爆" in err_msg:
                return "error", "查询暂时繁忙，请稍后重试"
            return "closed", err_msg

        if data.get("errorCode") == "00000" and data.get("status") == "SUCCESS":
            datas = data.get("datas", {})
            if not datas:
                return "empty", None
            if isinstance(datas, dict):
                order_list = datas.get("data") or datas.get("list") or datas.get("resultList")
                if isinstance(order_list, list) and order_list:
                    return "orders", order_list
                if datas.get("conditionalUuid") or datas.get("uuid"):
                    return "orders", [datas]
                return "empty", None
            if isinstance(datas, list):
                return ("orders", datas) if datas else ("empty", None)

    # fallback: 旧格式兼容
    orders = []
    if isinstance(data, dict):
        order_list = data.get("data") or data.get("list") or data.get("resultList")
        if isinstance(order_list, list):
            orders = order_list
        elif isinstance(order_list, dict):
            orders = order_list.get("data") or order_list.get("list") or []
        else:
            orders = [data] if data.get("conditionalUuid") or data.get("uuid") else []
    elif isinstance(data, list):
        orders = data

    return ("orders", orders) if orders else ("empty", None)


def _order_table_rows(bank_name: str, orders: list, max_per_bank: int = 10):
    """把某家银行的订单列表转成 Markdown 表格数据行（不含表头）。"""
    rows = []
    for order in orders[:max_per_bank]:
        status = _status_label(order.get("status") or order.get("conditionalStatus")) or "-"
        trade_type = _trade_type_label(
            order.get("tradeType") or order.get("conditionalType") or order.get("ruleType")
        ) or "-"
        target_price = (order.get("targetPrice") or order.get("conditionalPrice")
                        or order.get("orderPrice") or "-")
        amount = order.get("amount") or order.get("gram") or order.get("orderGram") or "-"
        order_amount = order.get("orderAmount") or "-"
        create_time = _fmt_ts(order.get("createTime") or order.get("createdTime")) or "-"
        rows.append(
            f"| {bank_name} | {status} | {trade_type} | {target_price} | "
            f"{amount} | {order_amount} | {create_time} |"
        )
    return rows


def render_conditional_list(bank_code: str, data: dict) -> str:
    """渲染单个银行的条件单列表（Markdown 表格）。"""
    bank_name = BANK_CONFIG.get(bank_code, {}).get("name", bank_code)
    kind, payload = _parse_bank_result(bank_code, data)

    if kind == "error":
        return f"⚠️ 【{bank_name}】查询失败：{payload}"
    if kind == "closed":
        return f"【{bank_name}】{payload}，无条件单"
    if kind == "empty":
        return f"【{bank_name}】无条件单"

    orders = payload
    rows = _order_table_rows(bank_name, orders)
    lines = [f"📋 **【{bank_name}】共 {len(orders)} 个条件单**", "", _TABLE_HEADER, _TABLE_DIVIDER]
    lines.extend(rows)
    remaining = len(orders) - len(rows)
    if remaining > 0:
        lines.append(f"\n> 还有 {remaining} 个条件单未展示")
    return "\n".join(lines)


def render_all_conditional_lists(results: Dict[str, dict]) -> str:
    """渲染所有银行的条件单列表汇总（统一 Markdown 表格 + 三态备注）。"""
    if not results:
        return "当前无条件单"

    table_rows = []          # 汇总到一张表的所有订单行
    order_banks = []         # 有条件单的银行名
    empty_banks = []         # 确实无条件单/未开户的银行名
    error_banks = []         # 查询失败（服务异常）的银行 (名, 原因)

    for bank_code in ["CMBC", "CIB", "CITIC", "CZB"]:
        if bank_code not in results:
            continue
        bank_name = BANK_CONFIG.get(bank_code, {}).get("name", bank_code)
        kind, payload = _parse_bank_result(bank_code, results[bank_code])
        if kind == "error":
            error_banks.append((bank_name, payload))
        elif kind == "closed":
            empty_banks.append(f"{bank_name}（{payload}）")
        elif kind == "empty":
            empty_banks.append(bank_name)
        else:  # orders
            order_banks.append(bank_name)
            table_rows.extend(_order_table_rows(bank_name, payload))

    parts = []

    # 1) 有条件单 → 输出统一表格
    if table_rows:
        parts.append(f"📋 **您当前共有 {len(table_rows)} 个生效中的条件单**")
        parts.append("")
        parts.append(_TABLE_HEADER)
        parts.append(_TABLE_DIVIDER)
        parts.extend(table_rows)

    # 2) 无条件单的银行 → 一行备注
    if empty_banks:
        parts.append("")
        parts.append(f"ℹ️ 无条件单：{'、'.join(empty_banks)}")

    # 3) 查询失败的银行 → 单独提示，绝不并入"无条件单"
    if error_banks:
        parts.append("")
        for name, reason in error_banks:
            parts.append(f"⚠️ 【{name}】查询失败：{reason}")
        parts.append("> 以上「查询失败」的银行无法确认是否有条件单，请稍后重试。")

    # 全部正常且都无条件单
    if not table_rows and not error_banks:
        return "当前无条件单"

    return "\n".join(parts)


# ── CLI ─────────────────────────────────────────────────────────────


def main(argv=None):
    p = argparse.ArgumentParser(description="查询黄金条件单")
    p.add_argument("--bank", "-b", metavar="BANK_CODE",
                   help="指定银行(CMBC/CIB/CITIC/CZB)，默认查所有")
    p.add_argument("--status", "-s", metavar="STATUS",
                   help="条件单状态(1=生效中/2=已触发/3=已失效/4=已取消/5=已完成)，默认1")
    p.add_argument("--json", action="store_true", help="输出原始JSON")
    p.add_argument("--detail", "-d", action="store_true", help="查详情(需提供订单号)")
    p.add_argument("--trade-no", metavar="TRADE_NO", help="交易号(查详情时)")
    p.add_argument("--uuid", metavar="UUID", help="条件单UUID(查详情时)")
    p.add_argument("--claw", help="上报客户端 claw 类型（如 codex、openclaw）")
    args = p.parse_args(argv)
    bff_client.set_claw(args.claw)

    if args.json:
        if args.bank:
            bank = args.bank.upper()
            config = BANK_CONFIG.get(bank)
            if not config:
                print(f"不支持的银行: {args.bank}", file=sys.stderr)
                return 2
            try:
                if bank == "CMBC":
                    data = fetch_cmbc_conditional_list(status_list=[args.status or "1"])
                elif bank in ("CIB", "CITIC"):
                    data = fetch_std_conditional_list(bank, status_list=[args.status or "1"])
                elif bank == "CZB":
                    data = fetch_czb_conditional_list(status_list=[args.status or "1"])
            except Exception as e:
                data = {"__error__": str(e)}
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            all_data = fetch_all_conditional_lists(status_list=[args.status or "1"])
            print(json.dumps(all_data, ensure_ascii=False, indent=2))
        return 0

    if args.bank:
        bank = args.bank.upper()
        config = BANK_CONFIG.get(bank)
        if not config:
            print(f"不支持的银行: {args.bank}，支持: CMBC/CIB/CITIC/CZB", file=sys.stderr)
            return 2
        
        try:
            if bank == "CMBC":
                data = fetch_cmbc_conditional_list(status_list=[args.status or "1"])
            elif bank in ("CIB", "CITIC"):
                data = fetch_std_conditional_list(bank, status_list=[args.status or "1"])
            elif bank == "CZB":
                data = fetch_czb_conditional_list(status_list=[args.status or "1"])
            
            if data:
                print(render_conditional_list(bank, data))
            else:
                print(f"【{config['name']}】条件单查询返回空数据")
        except bff_client.BffError as e:
            if getattr(e, "code", None) == 403:
                print(e.message)
            else:
                print(f"条件单查询失败: {e}")
            return 3
        except RuntimeError as e:
            err_msg = str(e)
            if "未登录" in err_msg:
                print("请先完成登录授权", file=sys.stderr)
                return 10
            print(f"条件单查询失败: {e}")
            return 3
    else:
        try:
            all_data = fetch_all_conditional_lists(status_list=[args.status or "1"])
            print(render_all_conditional_lists(all_data))
        except bff_client.BffError as e:
            if getattr(e, "code", None) == 403:
                print(e.message)
            else:
                print(f"条件单查询失败: {e}")
            return 3
        except RuntimeError as e:
            err_msg = str(e)
            if "未登录" in err_msg:
                print("请先完成登录授权", file=sys.stderr)
                return 10
            print(f"条件单查询失败: {e}")
            return 3

    return 0


if __name__ == "__main__":
    sys.exit(main())