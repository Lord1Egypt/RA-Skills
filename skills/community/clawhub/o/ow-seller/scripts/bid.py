#!/usr/bin/env python3
"""
OWS - 准备并投标准备
根据买家需求准备投标资料
"""

import json
import pathlib
import sys
from datetime import datetime

STATE_DIR = pathlib.Path(__file__).resolve().parent.parent / "state"
BIDS_DIR = STATE_DIR / "bids"
OPPS_DIR = STATE_DIR / "opportunities"

def load_seller_config():
    """加载卖家配置"""
    config_file = STATE_DIR / "seller_config.json"
    if config_file.exists():
        return json.loads(config_file.read_text())
    return None

def calculate_optimal_price(buyer_budget, my_cost, min_margin=0.15):
    """计算最优报价"""
    min_price = my_cost * (1 + min_margin)
    
    if buyer_budget and buyer_budget > min_price * 1.5:
        # 预算充足，定价为预算的 65%
        target_price = buyer_budget * 0.65
    else:
        # 预算紧张，定价接近成本
        target_price = min_price
    
    return round(target_price, 2)

def prepare_bid(request_id, seller_config):
    """准备投标文件"""
    # 加载需求
    req_file = OPPS_DIR / f"{request_id}.json"
    if not req_file.exists():
        return {"error": f"未找到需求 {request_id}"}
    
    request = json.loads(req_file.read_text())
    
    # 生成投标
    bid = {
        "bid_id": f"BID-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "req_id": request_id,
        "created_at": datetime.now().isoformat(),
        "status": "draft",
        "supplier": {
            "name": seller_config.get("seller_name", "卖家"),
            "agent_id": seller_config.get("seller_id", "agent-xxx"),
            "contact": seller_config.get("contact", "")
        },
        "price": {
            "amount": calculate_optimal_price(
                request.get("budget_max"),
                seller_config.get("cost", 1000)
            ),
            "currency": "CNY",
            "includes_shipping": True
        },
        "auth_docs": seller_config.get("credentials", []),
        "delivery": {
            "time_days": 3,
            "method": "顺丰快递",
            "tracking_available": True
        },
        "reputation": seller_config.get("reputation", {
            "total_transactions": 100,
            "success_rate": 0.98,
            "disputes": 0,
            "platform_verified": True
        }),
        "warranty": {
            "return_policy": "7 天无理由退货",
            "refund_policy": "质量问题全额退款"
        }
    }
    
    return bid

def submit_bid(bid, platform="ow"):
    """提交投标"""
    # 这里应该调用平台 API 提交投标
    # 目前先保存到本地
    BIDS_DIR.mkdir(parents=True, exist_ok=True)
    bid_file = BIDS_DIR / f"{bid['bid_id']}.json"
    bid_file.write_text(json.dumps(bid, indent=2, ensure_ascii=False))
    
    return {
        "success": True,
        "bid_id": bid["bid_id"],
        "message": "投标已保存（演示模式）"
    }

def format_bid(bid):
    """格式化投标预览"""
    output = "📋 投标方案预览\n\n"
    output += f"投标 ID: {bid['bid_id']}\n"
    output += f"供应商：{bid['supplier']['name']}\n"
    output += f"报价：¥{bid['price']['amount']}\n"
    output += f"到货时间：{bid['delivery']['time_days']}天\n"
    output += f"资质文件：{len(bid['auth_docs'])}项\n"
    output += f"信誉评分：{bid['reputation'].get('success_rate', 0) * 100:.0f}% 好评\n"
    return output

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="准备投标")
    parser.add_argument("request_id", help="需求 ID")
    parser.add_argument("--submit", "-s", action="store_true", help="直接提交")
    
    args = parser.parse_args()
    
    seller_config = load_seller_config()
    if not seller_config:
        print("❌ 未找到卖家配置，请先配置卖家信息")
        sys.exit(1)
    
    bid = prepare_bid(args.request_id, seller_config)
    
    if "error" in bid:
        print(f"❌ {bid['error']}")
        sys.exit(1)
    
    print(format_bid(bid))
    
    if args.submit:
        result = submit_bid(bid)
        print(f"\n✅ {result['message']}")
        print(f"投标 ID: {result['bid_id']}")

if __name__ == "__main__":
    main()