#!/usr/bin/env python3
"""
全球采购招投标评标脚本
计算五维度综合得分并排序
评标完成后自动通知买家机器人
展示卖家信用信息（可选功能）
"""

import json
import pathlib
from datetime import datetime
from typing import Dict, List, Any

STATE_DIR = pathlib.Path(__file__).resolve().parent.parent / "state"

# 信用系统为可选功能，不修改 sys.path
# 信用系统需要单独安装：npx skills add Enze-dai/ow-skills/ow-credit
CREDIT_SYSTEM_ENABLED = False
format_seller_credit_display = None
get_credit_warning = None
get_seller_profile = None

def get_simple_credit_display(seller_id: str) -> str:
    """简化版信用信息显示（当信用系统未安装时）"""
    return f"📊 信用系统未安装，无法显示信用信息\n   安装：npx skills add Enze-dai/ow-skills/ow-credit"

def calculate_price_score(bids: List[Dict]) -> Dict[str, float]:
    """计算价格得分 (权重50%)"""
    min_price = min(b["price"]["amount"] for b in bids)
    scores = {}
    for bid in bids:
        bid_id = bid["bid_id"]
        price = bid["price"]["amount"]
        # 最低价满分，其他按比例递减
        score = (min_price / price) * 100
        scores[bid_id] = score * 0.5  # 加权
    return scores

def calculate_media_score(bids: List[Dict]) -> Dict[str, float]:
    """计算商品展示得分 (权重15%)"""
    scores = {}
    for bid in bids:
        bid_id = bid["bid_id"]
        
        # 图片得分（每张5分，上限15分）
        images = bid.get("images", [])
        image_score = min(len(images) * 5, 15)
        
        # 视频得分（有视频+10分）
        video_score = 10 if bid.get("video") else 0
        
        total = min(image_score + video_score, 15)
        scores[bid_id] = total  # 已经是15%权重内的分数
    
    return scores

def calculate_auth_score(bids: List[Dict]) -> Dict[str, float]:
    """计算真品证明得分 (权重20%)"""
    # 证明文件分值
    doc_values = {
        "business_license": 20,
        "agency_cert": 20,
        "auth_letter": 15,
        "quality_report": 15,
        "import_doc": 15,
        "store_photo": 10,
        "invoice_sample": 5,
        "other": 5
    }
    
    scores = {}
    for bid in bids:
        bid_id = bid["bid_id"]
        total = 0
        for doc in bid.get("auth_docs", []):
            doc_type = doc.get("type", "other")
            total += doc_values.get(doc_type, 5)
        total = min(total, 100)  # 上限100
        scores[bid_id] = total * 0.2  # 加权
    return scores

def calculate_delivery_score(bids: List[Dict]) -> Dict[str, float]:
    """计算到货时间得分 (权重5%)"""
    min_days = min(b["delivery"]["time_days"] for b in bids)
    scores = {}
    for bid in bids:
        bid_id = bid["bid_id"]
        days = bid["delivery"]["time_days"]
        score = (min_days / days) * 100
        scores[bid_id] = score * 0.05  # 加权
    return scores

def calculate_reputation_score(bids: List[Dict]) -> Dict[str, float]:
    """计算交易记录得分 (权重10%)"""
    scores = {}
    for bid in bids:
        bid_id = bid["bid_id"]
        rep = bid.get("reputation", {})
        
        # 成交次数分 (上限50)
        tx_score = min(rep.get("total_transactions", 0) * 2, 50)
        
        # 好评率分
        success_rate = rep.get("success_rate", 0.5)
        rate_score = success_rate * 30
        
        # 纠纷扣分
        dispute_penalty = rep.get("disputes", 0) * 5
        
        # 投诉扣分
        complaint_penalty = rep.get("complaints", 0) * 10
        
        # 平台认证加分
        verified_bonus = 10 if rep.get("platform_verified", False) else 0
        
        total = max(0, tx_score + rate_score - dispute_penalty - complaint_penalty + verified_bonus)
        total = min(total, 100)
        scores[bid_id] = total * 0.1  # 加权
    return scores

def evaluate_bids(req_id: str, notify_buyer: bool = True) -> Dict[str, Any]:
    """执行完整评标"""
    bids_dir = STATE_DIR / "bids" / req_id
    
    if not bids_dir.exists():
        return {"error": f"未找到需求 {req_id} 的投标"}
    
    # 加载所有投标
    bids = []
    for bid_file in bids_dir.glob("*.json"):
        bid = json.loads(bid_file.read_text())
        bids.append(bid)
    
    if not bids:
        return {"error": f"需求 {req_id} 暂无投标"}
    
    # 计算各维度得分
    price_scores = calculate_price_score(bids)
    media_scores = calculate_media_score(bids)
    auth_scores = calculate_auth_score(bids)
    delivery_scores = calculate_delivery_score(bids)
    reputation_scores = calculate_reputation_score(bids)
    
    # 计算综合得分
    results = []
    for bid in bids:
        bid_id = bid["bid_id"]
        total = (
            price_scores.get(bid_id, 0) +
            media_scores.get(bid_id, 0) +
            auth_scores.get(bid_id, 0) +
            delivery_scores.get(bid_id, 0) +
            reputation_scores.get(bid_id, 0)
        )
        
        results.append({
            "bid_id": bid_id,
            "supplier": bid["supplier"]["name"],
            "supplier_id": bid["supplier"].get("agent_id", bid["supplier"]["name"]),
            "price": bid["price"]["amount"],
            "price_score": price_scores.get(bid_id, 0),
            "media_score": media_scores.get(bid_id, 0),
            "auth_score": auth_scores.get(bid_id, 0),
            "delivery_days": bid["delivery"]["time_days"],
            "delivery_score": delivery_scores.get(bid_id, 0),
            "reputation_score": reputation_scores.get(bid_id, 0),
            "total_score": round(total, 2),
            "auth_docs": [d["name"] if isinstance(d, dict) else d for d in bid.get("auth_docs", [])],
            "images": bid.get("images", []),
            "video": bid.get("video"),
            "reputation": bid.get("reputation", {}),
            "shop_links": bid.get("shop_links", [])
        })
    
    # 按综合得分排序
    results.sort(key=lambda x: x["total_score"], reverse=True)
    
    # 取前三名
    top3 = results[:3]
    
    result = {
        "req_id": req_id,
        "total_bids": len(bids),
        "evaluated_at": datetime.now().isoformat(),
        "top3": top3,
        "all_results": results
    }
    
    # 保存结果
    result_file = STATE_DIR / "requirements" / f"{req_id}_result.json"
    result_file.parent.mkdir(parents=True, exist_ok=True)
    result_file.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 🔔 通知买家机器人（评标完成提醒）
    if notify_buyer:
        try:
            from notify import notify_on_evaluation
            notification = notify_on_evaluation(req_id, result)
            result["notification_sent"] = notification.get("delivered", False)
        except Exception as e:
            result["notification_error"] = str(e)
    
    return result

def format_result(result: Dict) -> str:
    """格式化评标结果输出"""
    if "error" in result:
        return f"❌ {result['error']}"
    
    output = f"📊 评标结果 - {result['req_id']}\n"
    output += f"投标总数: {result['total_bids']} | 评估时间: {result['evaluated_at']}\n\n"
    
    medals = ["🏆", "🥈", "🥉"]
    for i, bid in enumerate(result["top3"]):
        medal = medals[i]
        output += f"{medal} 第{i+1}名：{bid['supplier']} | 综合得分 {bid['total_score']}\n"
        output += f"   ├─ 💰 价格：¥{bid['price']} (得分 {bid['price_score']:.1f}/50)\n"
        output += f"   ├─ 📜 真品：{len(bid['auth_docs'])}项证明 (得分 {bid['auth_score']:.1f}/20)\n"
        output += f"   ├─ 📸 展示：{len(bid.get('images', []))}图+{'有视频' if bid.get('video') else '无视频'} (得分 {bid['media_score']:.1f}/15)\n"
        output += f"   ├─ 🚚 时效：{bid['delivery_days']}天 (得分 {bid['delivery_score']:.1f}/5)\n"
        output += f"   └─ 📋 信誉：{bid['reputation'].get('total_transactions', 0)}笔成交 (得分 {bid['reputation_score']:.1f}/10)\n"
        
        # 🛡️ 添加信用展示
        if CREDIT_SYSTEM_ENABLED:
            try:
                seller_id = bid.get('supplier_id', bid['supplier'])
                credit_display = format_seller_credit_display(seller_id)
                warning = get_credit_warning(seller_id, "seller")
                output += f"\n   ─── 信用信息 ───\n"
                for line in credit_display.strip().split('\n'):
                    output += f"   {line}\n"
                if warning:
                    output += f"   {warning}\n"
            except Exception as e:
                output += f"   ⚠️ 信用信息获取失败: {e}\n"
        
        output += "\n"
    
    if result.get("notification_sent"):
        output += "\n🔔 已通知买家机器人评标完成\n"
    
    return output

def main():
    if len(sys.argv) < 2:
        print("用法: python evaluate.py <req_id>")
        sys.exit(1)
    
    req_id = sys.argv[1]
    result = evaluate_bids(req_id)
    print(format_result(result))

if __name__ == "__main__":
    main()