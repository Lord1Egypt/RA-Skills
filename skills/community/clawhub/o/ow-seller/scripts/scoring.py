#!/usr/bin/env python3
"""
OWS 智能评分系统
计算投标综合得分
"""

import json
import pathlib
from datetime import datetime

STATE_DIR = pathlib.Path(__file__).resolve().parent.parent / "state"
BIDS_DIR = STATE_DIR / "bids"

def calculate_price_score(bid_price, budget_max, all_prices):
    """计算价格得分 (权重 35%)"""
    if not all_prices:
        return 35.0  # 无竞争，默认满分
    
    min_price = min(all_prices)
    
    # 价格竞争力公式
    if bid_price <= min_price:
        score = 35.0
    elif bid_price >= budget_max:
        score = 0
    else:
        # 线性插值
        score = 35.0 * (budget_max - bid_price) / (budget_max - min_price)
    
    return round(score, 2)

def calculate_auth_score(auth_docs):
    """计算真品证明得分 (权重 20%)"""
    doc_values = {
        "business_license": 5,      # 营业执照
        "agency_cert": 5,           # 代理权证明
        "auth_letter": 4,           # 授权书
        "quality_report": 3,        # 质检报告
        "import_doc": 3,            # 进口文件
    }
    
    total = 0
    for doc in auth_docs:
        doc_type = doc.get("type", "")
        total += doc_values.get(doc_type, 1)
    
    # 上限 20 分
    return min(total, 20)

def calculate_delivery_score(delivery_days, all_delivery_days):
    """计算到货时间得分 (权重 5%)"""
    if not all_delivery_days:
        return 5.0
    
    min_days = min(all_delivery_days)
    max_days = max(all_delivery_days)
    
    if min_days == max_days:
        return 5.0
    
    # 时间越短得分越高
    if delivery_days <= min_days:
        score = 5.0
    elif delivery_days >= max_days:
        score = 0
    else:
        score = 5.0 * (max_days - delivery_days) / (max_days - min_days)
    
    return round(score, 2)

def calculate_reputation_score(seller_profile):
    """计算商家信誉得分 (权重 10%)"""
    if not seller_profile:
        return 5.0  # 新商家默认 5 分
    
    score = 0
    
    # 成交笔数 (最多 3 分)
    total_sales = seller_profile.get("total_sales", 0)
    score += min(total_sales / 10, 3)
    
    # 好评率 (最多 4 分)
    good_rate = seller_profile.get("good_rate", 0)
    if good_rate >= 0.98:
        score += 4
    elif good_rate >= 0.95:
        score += 3
    elif good_rate >= 0.90:
        score += 2
    elif good_rate >= 0.80:
        score += 1
    
    # 纠纷扣分
    disputes = seller_profile.get("disputes", 0)
    score -= disputes * 2
    
    # 退货扣分
    returns = seller_profile.get("returns", 0)
    score -= returns * 0.5
    
    return max(0, min(10, round(score, 2)))

def calculate_media_score(bid_id):
    """计算媒体展示得分 (权重 20%)"""
    from media import get_media_score
    media_score = get_media_score(bid_id)
    return media_score["total_media_score"]

def calculate_transaction_score(seller_id):
    """计算过往交易记录得分 (权重 10%)"""
    profile_file = STATE_DIR / "seller_profiles" / f"{seller_id}.json"
    
    if not profile_file.exists():
        return 5.0  # 新卖家
    
    profile = json.loads(profile_file.read_text())
    
    score = 0
    
    # 成交笔数 (最多 5 分)
    total_sales = profile.get("total_sales", 0)
    score += min(total_sales / 10, 5)
    
    # 好评率 (最多 3 分)
    good_rate = profile.get("good_rate", 0)
    if good_rate >= 0.95:
        score += 3
    elif good_rate >= 0.90:
        score += 2
    elif good_rate >= 0.80:
        score += 1
    
    # 纠纷扣分
    disputes = profile.get("disputes", 0)
    score -= disputes * 2
    
    # 退货扣分
    returns = profile.get("returns", 0)
    score -= returns
    
    return max(0, min(10, round(score, 2)))

def calculate_total_score(bid_data, all_bids, seller_profile=None):
    """计算综合总分"""
    
    # 获取所有投标的价格和到货时间
    all_prices = [b["price"]["amount"] for b in all_bids if "price" in b]
    all_delivery_days = [b["delivery"]["time_days"] for b in all_bids if "delivery" in b]
    
    # 计算各维度得分
    scores = {
        "price": {
            "weight": 35,
            "score": calculate_price_score(
                bid_data["price"]["amount"],
                bid_data.get("budget_max", bid_data["price"]["amount"] * 2),
                all_prices
            )
        },
        "auth": {
            "weight": 20,
            "score": calculate_auth_score(bid_data.get("auth_docs", []))
        },
        "delivery": {
            "weight": 5,
            "score": calculate_delivery_score(
                bid_data["delivery"]["time_days"],
                all_delivery_days
            )
        },
        "reputation": {
            "weight": 10,
            "score": calculate_reputation_score(seller_profile)
        },
        "media": {
            "weight": 20,
            "score": calculate_media_score(bid_data["bid_id"])
        },
        "transaction": {
            "weight": 10,
            "score": calculate_transaction_score(bid_data["supplier"]["agent_id"])
        }
    }
    
    # 计算总分
    total = sum(s["score"] for s in scores.values())
    
    return {
        "bid_id": bid_data["bid_id"],
        "scores": scores,
        "total_score": round(total, 2),
        "grade": get_grade(total)
    }

def get_grade(score):
    """获取等级"""
    if score >= 90:
        return "A+ (优秀)"
    elif score >= 80:
        return "A (良好)"
    elif score >= 70:
        return "B (合格)"
    elif score >= 60:
        return "C (一般)"
    else:
        return "D (较差)"

def format_score_report(score_result):
    """格式化评分报告"""
    report = f"""
📊 投标评分报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

投标ID: {score_result['bid_id']}
综合得分: {score_result['total_score']}/100
等级: {score_result['grade']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
各项评分:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    for name, data in score_result['scores'].items():
        name_map = {
            "price": "💰 价格",
            "auth": "📜 真品证明",
            "delivery": "🚚 到货时间",
            "reputation": "⭐ 商家信誉",
            "media": "📸 商品展示",
            "transaction": "📋 交易记录"
        }
        report += f"{name_map.get(name, name)}: {data['score']:.1f}/{data['weight']}\n"
    
    report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return report

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="OWS 评分系统")
    parser.add_argument("--bid-id", required=True, help="投标ID")
    parser.add_argument("--compare", action="store_true", help="对比其他投标")
    
    args = parser.parse_args()
    
    # 加载投标数据
    bid_file = BIDS_DIR / f"{args.bid_id}.json"
    if not bid_file.exists():
        print(f"❌ 投标不存在: {args.bid_id}")
        return
    
    bid_data = json.loads(bid_file.read_text())
    
    # 加载所有投标用于对比
    all_bids = [bid_data]
    if args.compare:
        for bf in BIDS_DIR.glob("*.json"):
            b = json.loads(bf.read_text())
            if b.get("req_id") == bid_data.get("req_id"):
                all_bids.append(b)
    
    result = calculate_total_score(bid_data, all_bids)
    print(format_score_report(result))

if __name__ == "__main__":
    main()