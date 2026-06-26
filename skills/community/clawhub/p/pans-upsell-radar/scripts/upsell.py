#!/usr/bin/env python3
"""
pans-upsell-radar: AI算力销售增购机会雷达
识别扩容信号，发现增购机会
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

# 数据目录
DATA_DIR = Path.home() / ".qclaw" / "skills" / "pans-upsell-radar" / "data"
CUSTOMERS_FILE = DATA_DIR / "customers.json"
SIGNALS_FILE = DATA_DIR / "signals.json"
OPPORTUNITIES_FILE = DATA_DIR / "opportunities.json"


@dataclass
class UpsellSignal:
    """增购信号"""
    type: str  # gpu_util, queue_time, team_expansion, new_model, business_growth, new_region
    description: str
    severity: str  # high, medium, low
    detected_at: str
    value: Optional[float] = None  # 数值（如利用率百分比）


@dataclass
class CustomerOpportunity:
    """客户增购机会"""
    client_name: str
    signals: list
    score: str  # high, medium, low
    score_reasons: list
    suggested_action: str
    best_timing: str
    estimated_expansion: str  # 预估扩容规模


def init_data_dir():
    """初始化数据目录"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # 初始化示例数据（如果不存在）
    if not CUSTOMERS_FILE.exists():
        sample_customers = [
            {
                "name": "智谱AI",
                "industry": "大模型",
                "current_gpu": "A100 8卡",
                "team_size": 50,
                "monthly_spend": 150000,
                "last_contact": "2026-04-01"
            },
            {
                "name": "出门问问",
                "industry": "语音AI",
                "current_gpu": "A100 4卡",
                "team_size": 30,
                "monthly_spend": 80000,
                "last_contact": "2026-03-28"
            },
            {
                "name": "月之暗面",
                "industry": "大模型",
                "current_gpu": "H100 16卡",
                "team_size": 80,
                "monthly_spend": 350000,
                "last_contact": "2026-04-10"
            },
            {
                "name": "MiniMax",
                "industry": "多模态",
                "current_gpu": "A100 8卡",
                "team_size": 40,
                "monthly_spend": 180000,
                "last_contact": "2026-03-20"
            }
        ]
        with open(CUSTOMERS_FILE, "w", encoding="utf-8") as f:
            json.dump(sample_customers, f, ensure_ascii=False, indent=2)
    
    if not SIGNALS_FILE.exists():
        sample_signals = [
            {"client": "智谱AI", "type": "gpu_util", "value": 87.5, "severity": "high"},
            {"client": "智谱AI", "type": "team_expansion", "value": 15, "severity": "medium"},
            {"client": "出门问问", "type": "queue_time", "value": 45, "severity": "medium"},
            {"client": "月之暗面", "type": "new_model", "value": 1, "severity": "high"},
            {"client": "MiniMax", "type": "business_growth", "value": 35, "severity": "high"}
        ]
        with open(SIGNALS_FILE, "w", encoding="utf-8") as f:
            json.dump(sample_signals, f, ensure_ascii=False, indent=2)


def load_customers() -> list:
    """加载客户数据"""
    if not CUSTOMERS_FILE.exists():
        return []
    with open(CUSTOMERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_signals() -> list:
    """加载信号数据"""
    if not SIGNALS_FILE.exists():
        return []
    with open(SIGNALS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_client_signals(client_name: str) -> list:
    """获取指定客户的信号"""
    signals = load_signals()
    return [s for s in signals if s.get("client") == client_name]


def calculate_score(signals: list) -> tuple:
    """
    计算机会评分
    返回: (score, reasons)
    """
    score = "low"
    reasons = []
    
    # 信号权重
    signal_weights = {
        "gpu_util": 3,      # GPU利用率
        "queue_time": 2,     # 排队时间
        "team_expansion": 2, # 团队扩张
        "new_model": 3,     # 新模型发布
        "business_growth": 3, # 业务增长
        "new_region": 2     # 新区域
    }
    
    severity_weights = {"high": 3, "medium": 2, "low": 1}
    
    total_score = 0
    signal_types = set()
    
    for signal in signals:
        sig_type = signal.get("type", "")
        severity = signal.get("severity", "low")
        value = signal.get("value", 0)
        
        signal_types.add(sig_type)
        total_score += signal_weights.get(sig_type, 1) * severity_weights.get(severity, 1)
        
        # 生成原因说明
        if sig_type == "gpu_util" and value > 80:
            reasons.append(f"GPU利用率高达{value}%，接近瓶颈")
        elif sig_type == "queue_time" and value > 30:
            reasons.append(f"任务排队时间增加{value}分钟")
        elif sig_type == "team_expansion":
            reasons.append(f"团队扩张{value}人")
        elif sig_type == "new_model":
            reasons.append("新模型发布需要更大算力")
        elif sig_type == "business_growth":
            reasons.append(f"业务增长{value}%")
        elif sig_type == "new_region":
            reasons.append("新区域/新场景需求")
    
    # 评分判定
    if total_score >= 8 or len(signal_types) >= 3:
        score = "high"
        reasons.append("多项信号叠加，决策窗口期")
    elif total_score >= 4 or len(signal_types) >= 2:
        score = "medium"
        reasons.append("存在明确增购信号")
    else:
        reasons.append("潜在需求，持续观察")
    
    return score, reasons


def generate_suggestion(client_name: str, score: str, current_gpu: str) -> list:
    """生成扩容建议"""
    suggestions = {
        "high": [
            "立即安排客户拜访",
            "准备扩容方案和报价",
            "强调新GPU型号的优势（H100/A100）",
            "提供试用机会降低决策门槛"
        ],
        "medium": [
            "保持定期沟通",
            "分享行业案例和最佳实践",
            "关注信号变化趋势"
        ],
        "low": [
            "纳入培育名单",
            "定期发送产品更新",
            "邀请参加技术分享活动"
        ]
    }
    
    gpu_suggestions = {
        "A100 4卡": "建议升级到A100 8卡或H100",
        "A100 8卡": "建议扩展到16卡集群或H100",
        "H100 16卡": "建议考虑多集群方案或H200"
    }
    
    actions = suggestions.get(score, suggestions["low"])
    if current_gpu in gpu_suggestions:
        actions.insert(0, gpu_suggestions[current_gpu])
    
    return actions


def get_best_timing(score: str) -> str:
    """预测最佳跟进时机"""
    timings = {
        "high": "立即（本周内）",
        "medium": "近期（2周内）",
        "low": "按季度跟进"
    }
    return timings.get(score, "待定")


def analyze_client(client_name: str, customers: list) -> Optional[CustomerOpportunity]:
    """分析单个客户"""
    # 查找客户
    client = None
    for c in customers:
        if c["name"] == client_name:
            client = c
            break
    
    if not client:
        print(f"未找到客户: {client_name}")
        return None
    
    # 获取信号
    signals = get_client_signals(client_name)
    
    # 计算评分
    score, reasons = calculate_score(signals)
    
    # 生成建议
    actions = generate_suggestion(client_name, score, client.get("current_gpu", ""))
    
    # 预估扩容规模
    expansion_map = {
        "high": "50%-100%扩容",
        "medium": "25%-50%扩容",
        "low": "10%-25%扩容"
    }
    
    return CustomerOpportunity(
        client_name=client_name,
        signals=signals,
        score=score,
        score_reasons=reasons,
        suggested_action="\n  • ".join(actions),
        best_timing=get_best_timing(score),
        estimated_expansion=expansion_map.get(score, "待评估")
    )


def scan_all_clients(customers: list) -> list:
    """扫描所有客户"""
    opportunities = []
    for client in customers:
        opp = analyze_client(client["name"], customers)
        if opp:
            opportunities.append(opp)
    # 按评分排序
    score_order = {"high": 0, "medium": 1, "low": 2}
    opportunities.sort(key=lambda x: score_order.get(x.score, 3))
    return opportunities


def format_opportunity(opp: CustomerOpportunity, detailed: bool = False) -> str:
    """格式化输出机会信息"""
    score_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    emoji = score_emoji.get(opp.score, "⚪")
    
    lines = [
        f"\n{emoji} {opp.client_name} [{opp.score.upper()}评分]",
        f"   预估扩容: {opp.estimated_expansion}",
        f"   最佳时机: {opp.best_timing}"
    ]
    
    if detailed:
        lines.append(f"   信号原因:")
        for reason in opp.score_reasons:
            lines.append(f"     • {reason}")
        lines.append(f"   建议行动:")
        lines.append(f"   • {opp.suggested_action}")
    
    return "\n".join(lines)


def cmd_scan():
    """扫描所有客户"""
    customers = load_customers()
    opportunities = scan_all_clients(customers)
    
    print("\n" + "="*50)
    print("🔍 AI算力销售增购机会扫描报告")
    print(f"   生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*50)
    
    if not opportunities:
        print("\n暂无增购机会")
        return
    
    # 按评分分组显示
    for score_level in ["high", "medium", "low"]:
        level_opps = [o for o in opportunities if o.score == score_level]
        if level_opps:
            print(f"\n【{score_level.upper()}优先级】")
            for opp in level_opps:
                print(format_opportunity(opp, detailed=True))
    
    print("\n" + "="*50)
    print(f"共发现 {len(opportunities)} 个增购机会")


def cmd_client(client_name: str):
    """分析指定客户"""
    customers = load_customers()
    opp = analyze_client(client_name, customers)
    
    if not opp:
        return
    
    print("\n" + "="*50)
    print(f"📊 客户分析: {client_name}")
    print("="*50)
    print(format_opportunity(opp, detailed=True))
    print("="*50)


def cmd_list():
    """列出增购机会"""
    customers = load_customers()
    opportunities = scan_all_clients(customers)
    
    print("\n📋 增购机会列表")
    print("-"*50)
    
    if not opportunities:
        print("暂无增购机会")
        return
    
    print(f"{'客户名称':<15} {'评分':<8} {'预估扩容':<15} {'最佳时机':<12}")
    print("-"*50)
    
    for opp in opportunities:
        print(f"{opp.client_name:<15} {opp.score.upper():<8} {opp.estimated_expansion:<15} {opp.best_timing:<12}")
    
    print("-"*50)
    print(f"共 {len(opportunities)} 个机会")


def cmd_score():
    """显示机会评分"""
    customers = load_customers()
    opportunities = scan_all_clients(customers)
    
    print("\n📈 机会评分详情")
    print("="*50)
    
    for opp in opportunities:
        print(format_opportunity(opp, detailed=False))
    
    print("\n评分标准:")
    print("  🔴 HIGH: 多信号叠加，决策窗口期，需立即跟进")
    print("  🟡 MEDIUM: 单一明确信号，持续观察")
    print("  🟢 LOW: 潜在需求，培育阶段")


def cmd_suggest():
    """生成增购方案"""
    customers = load_customers()
    opportunities = scan_all_clients(customers)
    
    print("\n💡 AI算力增购方案建议")
    print("="*50)
    
    high_opps = [o for o in opportunities if o.score == "high"]
    medium_opps = [o for o in opportunities if o.score == "medium"]
    
    print("\n【高优先级客户 - 立即行动】")
    if high_opps:
        for opp in high_opps:
            print(f"\n{opp.client_name}:")
            print(f"  当前状态: {opp.score_reasons[0] if opp.score_reasons else '多信号叠加'}")
            print(f"  建议方案: {opp.suggested_action.split(chr(10))[0]}")
            print(f"  预计成交周期: 1-2周")
    else:
        print("  暂无高优先级客户")
    
    print("\n\n【中优先级客户 - 持续跟进】")
    if medium_opps:
        for opp in medium_opps:
            print(f"\n{opp.client_name}:")
            print(f"  当前状态: {opp.score_reasons[0] if opp.score_reasons else '存在信号'}")
            print(f"  建议方案: {opp.suggested_action.split(chr(10))[0]}")
            print(f"  预计成交周期: 2-4周")
    else:
        print("  暂无中优先级客户")
    
    print("\n\n【整体建议】")
    print("  1. 优先拜访高优先级客户，争取本周完成初次沟通")
    print("  2. 为高优先级客户准备定制化扩容方案")
    print("  3. 整理成功案例和ROI数据，辅助客户决策")
    print("  4. 关注新模型发布动态，及时捕捉增购信号")


def main():
    parser = argparse.ArgumentParser(
        description="pans-upsell-radar: AI算力销售增购机会雷达"
    )
    parser.add_argument("--scan", action="store_true", help="扫描所有客户")
    parser.add_argument("--client", type=str, help="分析指定客户")
    parser.add_argument("--list", action="store_true", help="列出增购机会")
    parser.add_argument("--score", action="store_true", help="显示机会评分")
    parser.add_argument("--suggest", action="store_true", help="生成增购方案")
    
    args = parser.parse_args()
    
    # 初始化数据
    init_data_dir()
    
    # 如果没有参数，显示帮助
    if not any([args.scan, args.client, args.list, args.score, args.suggest]):
        parser.print_help()
        print("\n\n📌 示例用法:")
        print("  python upsell.py --list      # 列出所有机会")
        print("  python upsell.py --scan     # 扫描所有客户")
        print("  python upsell.py --client 智谱AI  # 分析指定客户")
        print("  python upsell.py --score    # 显示评分详情")
        print("  python upsell.py --suggest  # 生成增购方案")
        return
    
    # 执行命令
    if args.scan:
        cmd_scan()
    elif args.client:
        cmd_client(args.client)
    elif args.list:
        cmd_list()
    elif args.score:
        cmd_score()
    elif args.suggest:
        cmd_suggest()


if __name__ == "__main__":
    main()
