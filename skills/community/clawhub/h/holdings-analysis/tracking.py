#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票推荐追踪系统
- 记录推荐历史
- 追踪推荐后表现
- 触发卖出提醒
"""
import pandas as pd
import json
from pathlib import Path
from datetime import datetime, timedelta

DATA_DIR = Path(__file__).parent / "data"
TRACKING_FILE = DATA_DIR / "recommendation_tracking.json"


def load_tracking():
    """加载追踪数据"""
    if TRACKING_FILE.exists():
        with open(TRACKING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"recommendations": [], "history": []}


def save_tracking(data):
    """保存追踪数据"""
    TRACKING_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TRACKING_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def calc_stop_levels(score, volatility=0):
    """
    根据评分动态计算止盈止损
    
    参数:
    - score: 推荐评分 (60-100)
    - volatility: 波动率（可选，暂未使用）
    
    返回:
    - (止盈%, 止损%)
    """
    if score >= 100:
        return (20, 10)  # 高确定性，给更多空间
    elif score >= 90:
        return (15, 8)   # 默认标准
    elif score >= 80:
        return (12, 7)   # 中等确定性
    else:
        return (10, 5)   # 低确定性，快速止损


def add_recommendation(code, name, score, price, industry, stop_profit=None, stop_loss=None):
    """
    添加推荐记录
    
    参数:
    - code: 股票代码
    - name: 股票名称
    - score: 推荐评分
    - price: 推荐价格
    - industry: 行业
    - stop_profit: 止盈比例（默认自动计算）
    - stop_loss: 止损比例（默认自动计算）
    """
    data = load_tracking()
    
    # 检查是否已存在（7天内不重复推荐）
    for rec in data["recommendations"]:
        if rec["code"] == code:
            rec_date = datetime.fromisoformat(rec["recommend_date"])
            if (datetime.now() - rec_date).days < 7:
                return False  # 已存在且未过期
    
    # 自动计算止盈止损
    if stop_profit is None or stop_loss is None:
        stop_profit, stop_loss = calc_stop_levels(score)
    
    rec = {
        "code": code,
        "name": name,
        "industry": industry,
        "score": score,
        "recommend_price": price,
        "recommend_date": datetime.now().strftime("%Y-%m-%d"),
        "stop_profit_price": round(price * (1 + stop_profit / 100), 2),
        "stop_loss_price": round(price * (1 - stop_loss / 100), 2),
        "stop_profit_pct": stop_profit,
        "stop_loss_pct": stop_loss,
        "status": "active",  # active, profit, loss, expired
        "current_price": price,
        "current_gain_pct": 0,
        "max_gain_pct": 0,
        "min_gain_pct": 0,
        "update_count": 0,
    }
    
    data["recommendations"].append(rec)
    save_tracking(data)
    return True


def update_tracking(code, current_price):
    """更新追踪数据"""
    data = load_tracking()
    
    for rec in data["recommendations"]:
        if rec["code"] == code and rec["status"] == "active":
            rec["current_price"] = current_price
            gain = (current_price / rec["recommend_price"] - 1) * 100
            rec["current_gain_pct"] = round(gain, 2)
            rec["max_gain_pct"] = max(rec["max_gain_pct"], gain)
            rec["min_gain_pct"] = min(rec["min_gain_pct"], gain)
            rec["update_count"] += 1
            rec["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # 检查是否触发止盈止损
            if gain >= rec["stop_profit_pct"]:
                rec["status"] = "profit"
            elif gain <= -rec["stop_loss_pct"]:
                rec["status"] = "loss"
            
            save_tracking(data)
            return rec
    
    return None


def get_active_recommendations():
    """获取当前活跃的推荐"""
    data = load_tracking()
    active = [rec for rec in data["recommendations"] if rec["status"] == "active"]
    
    # 检查是否过期（推荐后20天自动过期）
    for rec in active:
        rec_date = datetime.fromisoformat(rec["recommend_date"])
        if (datetime.now() - rec_date).days > 20:
            rec["status"] = "expired"
    
    save_tracking(data)
    return [rec for rec in data["recommendations"] if rec["status"] == "active"]


def get_triggered_alerts():
    """获取触发卖出提醒的股票"""
    data = load_tracking()
    alerts = []
    
    for rec in data["recommendations"]:
        if rec["status"] == "active":
            gain = rec["current_gain_pct"]
            
            # 止盈提醒
            if gain >= rec["stop_profit_pct"]:
                alerts.append({
                    "type": "profit",
                    "code": rec["code"],
                    "name": rec["name"],
                    "recommend_price": rec["recommend_price"],
                    "current_price": rec["current_price"],
                    "gain_pct": gain,
                    "message": f"触发止盈 (+{gain:.1f}% >= +{rec['stop_profit_pct']}%)"
                })
            
            # 止损提醒
            elif gain <= -rec["stop_loss_pct"]:
                alerts.append({
                    "type": "loss",
                    "code": rec["code"],
                    "name": rec["name"],
                    "recommend_price": rec["recommend_price"],
                    "current_price": rec["current_price"],
                    "gain_pct": gain,
                    "message": f"触发止损 ({gain:.1f}% <= -{rec['stop_loss_pct']}%)"
                })
    
    return alerts


def generate_tracking_report():
    """生成追踪报告"""
    data = load_tracking()
    
    if not data["recommendations"]:
        return "暂无推荐记录"
    
    total = len(data["recommendations"])
    active = len([r for r in data["recommendations"] if r["status"] == "active"])
    profit = len([r for r in data["recommendations"] if r["status"] == "profit"])
    loss = len([r for r in data["recommendations"] if r["status"] == "loss"])
    expired = len([r for r in data["recommendations"] if r["status"] == "expired"])
    
    # 计算平均收益
    completed = [r for r in data["recommendations"] if r["status"] in ["profit", "loss", "expired"]]
    if completed:
        avg_gain = sum(r["current_gain_pct"] for r in completed) / len(completed)
    else:
        avg_gain = 0
    
    lines = []
    lines.append("📊 推荐追踪报告")
    lines.append(datetime.now().strftime("%Y-%m-%d"))
    lines.append("──────────────")
    lines.append("")
    lines.append(f"📈 总推荐: {total}只")
    lines.append(f"✅ 活跃: {active}只")
    lines.append(f"🎯 止盈: {profit}只")
    lines.append(f"❌ 止损: {loss}只")
    lines.append(f"⏰ 过期: {expired}只")
    lines.append(f"📊 平均收益: {avg_gain:+.1f}%")
    lines.append("")
    
    # 显示活跃推荐
    if active > 0:
        lines.append("【当前持仓】")
        lines.append("")
        for rec in sorted(data["recommendations"], key=lambda x: x["recommend_date"], reverse=True):
            if rec["status"] != "active":
                continue
            
            days = (datetime.now() - datetime.fromisoformat(rec["recommend_date"])).days
            lines.append(f"📌 {rec['name']} {rec['code']}")
            lines.append(f"   推荐:{rec['recommend_price']}  现价:{rec['current_price']}")
            lines.append(f"   收益:{rec['current_gain_pct']:+.1f}%  持有:{days}天")
            lines.append(f"   止盈:+{rec['stop_profit_pct']}%  止损:-{rec['stop_loss_pct']}%")
            lines.append("")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # 测试
    print(generate_tracking_report())
