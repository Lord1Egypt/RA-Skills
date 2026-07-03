#!/usr/bin/env python3
"""
电商物流延迟检测引擎
- 查询物流轨迹（支持UAPI免费API）
- 延迟风险规则引擎
- 输出结构化检测结果
"""

import json
import os
import sys
import csv
import time
import argparse
from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import urlencode

try:
    import requests
except ImportError:
    print("[SETUP] 安装依赖: pip install requests")
    os.system(f"{sys.executable} -m pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn")
    import requests

# ============ 配置 ============

# UAPI 配置
UAPI_BASE_URL = "https://uapis.cn/api/v1/misc/tracking/query"
UAPI_API_KEY = os.environ.get("UAPI_API_KEY", "")  # 从环境变量或配置文件读取

# 延迟检测规则：{规则名: {condition_fields, threshold_hours, severity, description}}
DELAY_RULES = {
    "shipping_timeout": {
        "name": "发货超时",
        "threshold_hours": 48,
        "severity": "high",
        "icon": "🔴",
        "description": "下单超过{threshold}小时，物流仍为待揽件状态",
        "check": lambda t, o: (
            t.get("status") in ("pending", "created", "waiting_pickup", "待揽件", "已下单")
            and _hours_since(o.get("order_date")) > 48
        ),
    },
    "transit_stuck": {
        "name": "运输停滞",
        "threshold_hours": 24,
        "severity": "medium",
        "icon": "🟡",
        "description": "物流最近更新超过{threshold}小时，包裹在运输中停滞",
        "check": lambda t, o: (
            t.get("status") in ("in_transit", "transporting", "运输中")
            and _hours_since(t.get("last_update")) > 24
        ),
    },
    "delivery_problem": {
        "name": "派送异常",
        "threshold_hours": 0,
        "severity": "high",
        "icon": "🔴",
        "description": "物流状态异常：退回/丢失/损坏/拒收",
        "check": lambda t, o: t.get("status") in (
            "problem", "returned", "lost", "damaged", "rejected",
            "异常", "退回", "丢失", "损坏", "拒收",
        ),
    },
    "estimated_late": {
        "name": "预计超时",
        "threshold_hours": 0,
        "severity": "medium",
        "icon": "🟡",
        "description": "当前时间已超过预计送达时间，包裹未签收",
        "check": lambda t, o: (
            t.get("status") not in ("delivered", "signed", "已签收", "签收")
            and t.get("estimated_delivery")
            and _is_past(t.get("estimated_delivery"))
        ),
    },
    "no_tracking": {
        "name": "无物流信息",
        "threshold_hours": 24,
        "severity": "low",
        "icon": "🟢",
        "description": "运单号查询无结果，可能未揽件或单号错误",
        "check": lambda t, o: t.get("status") == "not_found",
    },
}


def _hours_since(date_str: Optional[str]) -> float:
    """计算从给定时间到现在的小时数"""
    if not date_str:
        return 999.0
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00").replace("+08:00", ""))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=None)
        return (datetime.now() - dt).total_seconds() / 3600
    except (ValueError, TypeError):
        return 999.0


def _is_past(date_str: str) -> bool:
    """判断日期是否已过"""
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00").replace("+08:00", ""))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=None)
        return dt < datetime.now()
    except (ValueError, TypeError):
        return False


# ============ 物流查询 ============

def query_uapi(tracking_number: str, carrier_code: str = "", phone: str = "") -> dict:
    """
    通过UAPI查询物流轨迹
    
    Args:
        tracking_number: 快递单号
        carrier_code: 快递公司编码（可选，不填自动识别）
        phone: 收件人手机尾号4位（部分快递需要）
    
    Returns:
        {
            "success": bool,
            "status": str,       # 物流状态
            "details": list,     # 轨迹详情
            "last_update": str,  # 最后更新时间
            "estimated_delivery": str | None,
            "carrier": str,      # 快递公司
            "error": str | None,
        }
    """
    if not UAPI_API_KEY:
        return {
            "success": False,
            "status": "config_error",
            "details": [],
            "last_update": None,
            "estimated_delivery": None,
            "carrier": "",
            "error": "未配置 UAPI_API_KEY，请在环境变量或 ~/.workbuddy/skills/logistics-care/references/api_config.md 中设置",
        }

    params = {
        "tracking_number": tracking_number,
    }
    if carrier_code:
        params["carrier_code"] = carrier_code
    if phone and len(phone) >= 4:
        params["phone"] = phone[-4:]

    headers = {
        "Authorization": f"Bearer {UAPI_API_KEY}",
        "Accept": "application/json",
    }

    try:
        url = f"{UAPI_BASE_URL}?{urlencode(params)}"
        resp = requests.get(url, headers=headers, timeout=15)
        
        if resp.status_code == 200:
            data = resp.json()
            return _parse_uapi_response(data, tracking_number, carrier_code)
        elif resp.status_code == 404:
            return {
                "success": True,
                "status": "not_found",
                "details": [],
                "last_update": None,
                "estimated_delivery": None,
                "carrier": carrier_code or "未知",
                "error": None,
            }
        else:
            return {
                "success": False,
                "status": "api_error",
                "details": [],
                "last_update": None,
                "estimated_delivery": None,
                "carrier": carrier_code or "",
                "error": f"API返回 {resp.status_code}: {resp.text[:200]}",
            }
    except requests.exceptions.Timeout:
        return {
            "success": False, "status": "timeout",
            "details": [], "last_update": None, "estimated_delivery": None,
            "carrier": carrier_code or "", "error": "请求超时",
        }
    except Exception as e:
        return {
            "success": False, "status": "network_error",
            "details": [], "last_update": None, "estimated_delivery": None,
            "carrier": carrier_code or "", "error": str(e),
        }


def _parse_uapi_response(data: dict, tracking_number: str, carrier_code: str) -> dict:
    """解析UAPI返回的物流数据"""
    try:
        # UAPI 返回结构：{ "code": 200, "data": { "tracking_number": ..., "status": ..., "details": [...], ... } }
        resp_data = data.get("data", data)
        
        details = resp_data.get("details", resp_data.get("traces", resp_data.get("tracking_details", [])))
        if isinstance(details, list):
            details = [
                {"time": d.get("time", d.get("ftime", "")), "desc": d.get("desc", d.get("context", ""))}
                for d in details
            ]
        
        # 获取最后更新时间
        last_update = None
        if details:
            last_update = details[0].get("time") or details[-1].get("time")
        
        # 解析状态
        raw_status = resp_data.get("status", resp_data.get("state", "")).lower()
        status = _normalize_status(raw_status)
        
        # 预估送达时间
        estimated = resp_data.get("estimated_delivery", resp_data.get("estimated_delivery_time", None))
        
        carrier = resp_data.get("carrier", resp_data.get("exp_name", carrier_code or "未知"))
        
        return {
            "success": True,
            "status": status,
            "details": details,
            "last_update": last_update,
            "estimated_delivery": str(estimated) if estimated else None,
            "carrier": str(carrier),
            "error": None,
        }
    except Exception as e:
        return {
            "success": False, "status": "parse_error",
            "details": [], "last_update": None, "estimated_delivery": None,
            "carrier": carrier_code or "", "error": f"解析失败: {e}",
        }


def _normalize_status(raw: str) -> str:
    """标准化物流状态"""
    status_map = {
        "pending": "pending", "created": "pending", "waiting_pickup": "pending",
        "待揽件": "pending", "已下单": "pending", "待取件": "pending",
        
        "in_transit": "in_transit", "transporting": "in_transit", "delivering": "in_transit",
        "运输中": "in_transit", "派送中": "in_transit", "转运中": "in_transit", "在途": "in_transit",
        
        "out_for_delivery": "out_for_delivery", "派送": "out_for_delivery",
        "快递员派送中": "out_for_delivery",
        
        "delivered": "delivered", "signed": "delivered",
        "已签收": "delivered", "签收": "delivered", "已送达": "delivered",
        
        "problem": "problem", "returned": "problem", "退回": "problem",
        "丢失": "problem", "lost": "problem", "异常": "problem",
        "damaged": "problem", "损坏": "problem",
    }
    return status_map.get(raw, raw)


# ============ 延迟检测 ============

def detect_delays(tracking_result: dict, order: dict) -> list:
    """
    检测物流延迟风险
    
    Args:
        tracking_result: query_uapi 的返回结果
        order: 订单信息字典
    
    Returns:
        [{"rule": str, "name": str, "severity": str, "icon": str, "description": str}, ...]
    """
    delays = []
    
    if not tracking_result["success"]:
        delays.append({
            "rule": "api_failed",
            "name": "API查询失败",
            "severity": "low",
            "icon": "🟢",
            "description": f"物流查询失败: {tracking_result.get('error', '未知错误')}",
        })
        return delays
    
    for rule_key, rule in DELAY_RULES.items():
        try:
            if rule["check"](tracking_result, order):
                desc = rule["description"].format(threshold=rule["threshold_hours"])
                delays.append({
                    "rule": rule_key,
                    "name": rule["name"],
                    "severity": rule["severity"],
                    "icon": rule["icon"],
                    "description": desc,
                })
        except Exception as e:
            # 规则检查异常，跳过
            pass
    
    # 按严重程度排序: high > medium > low
    severity_order = {"high": 0, "medium": 1, "low": 2}
    delays.sort(key=lambda d: severity_order.get(d["severity"], 3))
    
    return delays


# ============ 批量处理 ============

def read_orders_csv(csv_path: str) -> list:
    """读取订单CSV文件"""
    orders = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            orders.append({
                "order_id": row.get("order_id", "").strip(),
                "customer_name": row.get("customer_name", "").strip(),
                "customer_phone": row.get("customer_phone", "").strip(),
                "tracking_number": row.get("tracking_number", "").strip(),
                "carrier_code": row.get("carrier_code", "").strip(),
                "order_date": row.get("order_date", "").strip(),
                "product_name": row.get("product_name", "").strip(),
            })
    return orders


def validate_orders(orders: list) -> tuple:
    """验证订单数据，返回 (valid_orders, errors)"""
    valid = []
    errors = []
    required = ["order_id", "customer_phone", "tracking_number"]
    
    for i, order in enumerate(orders):
        missing = [f for f in required if not order.get(f)]
        if missing:
            errors.append({"row": i + 1, "order_id": order.get("order_id", "N/A"), "error": f"缺少必填字段: {', '.join(missing)}"})
            continue
        if not order["customer_phone"].isdigit() or len(order["customer_phone"]) != 11:
            errors.append({"row": i + 1, "order_id": order["order_id"], "error": f"手机号格式错误: {order['customer_phone']}"})
            continue
        if not order["tracking_number"].strip():
            errors.append({"row": i + 1, "order_id": order["order_id"], "error": "运单号为空"})
            continue
        valid.append(order)
    
    return valid, errors


def process_batch(orders: list, output_path: str, delay: float = 1.0) -> dict:
    """
    批量处理订单物流查询
    
    Args:
        orders: 订单列表
        output_path: 结果输出JSON路径
        delay: 每次查询间隔秒数（避免触发API限流）
    
    Returns:
        完整结果字典
    """
    results = {
        "generated_at": datetime.now().isoformat(),
        "total_orders": len(orders),
        "success_count": 0,
        "delayed_count": 0,
        "orders": [],
    }
    
    for i, order in enumerate(orders):
        print(f"[{i+1}/{len(orders)}] 查询 {order['tracking_number']} (订单 {order['order_id']})...")
        
        # 查询物流
        tracking = query_uapi(
            tracking_number=order["tracking_number"],
            carrier_code=order.get("carrier_code", ""),
            phone=order.get("customer_phone", ""),
        )
        
        # 检测延迟
        delays = detect_delays(tracking, order)
        
        # 判断整体状态
        has_delay = any(d["severity"] in ("high", "medium") for d in delays)
        overall_status = _get_overall_status(tracking, delays)
        
        order_result = {
            "order_id": order["order_id"],
            "customer_name": order["customer_name"],
            "customer_phone": order["customer_phone"],
            "tracking_number": order["tracking_number"],
            "product_name": order.get("product_name", ""),
            "order_date": order.get("order_date", ""),
            "tracking": tracking,
            "delays": delays,
            "has_delay": has_delay,
            "overall_status": overall_status,
        }
        results["orders"].append(order_result)
        
        if tracking["success"] and tracking["status"] != "config_error":
            results["success_count"] += 1
        if has_delay:
            results["delayed_count"] += 1
        
        # API限流
        if i < len(orders) - 1:
            time.sleep(delay)
    
    # 保存结果
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 打印摘要
    print(f"\n📊 检测完成:")
    print(f"   总订单: {results['total_orders']}")
    print(f"   查询成功: {results['success_count']}")
    print(f"   延迟风险: {results['delayed_count']}")
    print(f"   结果保存: {output_path}")
    
    return results


def _get_overall_status(tracking: dict, delays: list) -> str:
    """判断订单整体状态"""
    if not tracking["success"]:
        return "unknown"
    
    has_high = any(d["severity"] == "high" for d in delays)
    has_medium = any(d["severity"] == "medium" for d in delays)
    
    if tracking["status"] == "delivered":
        return "normal"
    if has_high:
        return "delayed_high"
    if has_medium:
        return "delayed_medium"
    if delays:
        return "delayed_low"
    return "normal"


# ============ 命令行 ============

def main():
    parser = argparse.ArgumentParser(description="电商物流延迟检测引擎")
    parser.add_argument("--input", "-i", required=True, help="订单CSV文件路径")
    parser.add_argument("--output", "-o", default="logistics_results.json", help="结果输出JSON路径")
    parser.add_argument("--validate", action="store_true", help="仅验证CSV格式，不查询物流")
    parser.add_argument("--delay", type=float, default=1.0, help="API查询间隔秒数（默认1秒）")
    parser.add_argument("--single", "-s", help="单号查询模式：快递单号")
    parser.add_argument("--carrier", "-c", default="", help="快递公司编码（单号模式）")
    parser.add_argument("--phone", "-p", default="", help="收件人手机尾号（单号模式）")
    
    args = parser.parse_args()
    
    # 配置检查
    if not UAPI_API_KEY:
        config_path = os.path.expanduser("~/.workbuddy/skills/logistics-care/references/api_config.md")
        print(f"⚠️  未配置 UAPI_API_KEY")
        print(f"   请在 {config_path} 中设置，或通过环境变量设置：")
        print(f"   export UAPI_API_KEY='your_key_here'")
        print(f"   免费注册: https://uapis.cn")
    
    # 单号模式
    if args.single:
        print(f"🔍 查询单号: {args.single}")
        result = query_uapi(args.single, args.carrier, args.phone)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        # 模拟订单信息用于延迟检测
        mock_order = {"order_date": datetime.now().isoformat()}
        delays = detect_delays(result, mock_order)
        if delays:
            print("\n🚨 延迟风险:")
            for d in delays:
                print(f"   {d['icon']} [{d['severity'].upper()}] {d['name']}: {d['description']}")
        else:
            print("\n✅ 未检测到延迟风险")
        return
    
    # CSV批量模式
    print(f"📋 读取订单: {args.input}")
    orders = read_orders_csv(args.input)
    valid_orders, errors = validate_orders(orders)
    
    if errors:
        print(f"\n⚠️  数据验证发现 {len(errors)} 个问题:")
        for e in errors:
            print(f"   第{e['row']}行({e['order_id']}): {e['error']}")
    
    if args.validate:
        print(f"\n✅ 验证完成: {len(valid_orders)}/{len(orders)} 条有效订单")
        return
    
    if not valid_orders:
        print("❌ 没有有效订单可处理")
        sys.exit(1)
    
    print(f"🔄 开始处理 {len(valid_orders)} 条有效订单...")
    process_batch(valid_orders, args.output, args.delay)


if __name__ == "__main__":
    main()
