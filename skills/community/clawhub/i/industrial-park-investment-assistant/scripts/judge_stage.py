#!/usr/bin/env python3
"""
客户阶段判断脚本
根据客户互动记录判断当前处于哪个阶段
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

# 阶段定义
STAGES = {
    1: "需求识别（首次接触，了解需求）",
    2: "房源匹配（提供方案，带看房源）",
    3: "方案对比（客户对比竞品，TCO分析）",
    4: "谈判（讨论条款，谈判租金/租期）",
    5: "决策（内部决策，审批流程）",
    6: "签约（签约成交，入驻准备）",
}

# 模拟客户数据（实际应从customers/客户档案.json读取）
SAMPLE_CUSTOMERS = {
    "测试科技公司": {
        "stage": 3,
        "stage_since": "2026-05-20",
        "interactions": [
            {"date": "2026-05-15", "type": "首次咨询", "content": "了解园区基本情况"},
            {"date": "2026-05-18", "type": "带看", "content": "看房T1栋8楼"},
            {"date": "2026-05-20", "type": "方案发送", "content": "发送报价方案"},
            {"date": "2026-05-25", "type": "电话沟通", "content": "讨论租金和竞品对比"},
        ],
        "decision_maker": "CEO",
        "intent_level": "A",
    }
}

def calculate_stage_duration(stage_since_str):
    """计算在当前阶段停留的时间"""
    stage_since = datetime.strptime(stage_since_str, "%Y-%m-%d")
    now = datetime.now()
    duration_days = (now - stage_since).days
    return duration_days

def judge_stage(customer_name):
    """判断客户阶段"""
    if customer_name not in SAMPLE_CUSTOMERS:
        return None, f"❌ 未找到客户: {customer_name}"
    
    customer = SAMPLE_CUSTOMERS[customer_name]
    stage = customer["stage"]
    stage_since_str = customer["stage_since"]
    
    # 计算停留时间
    duration_days = calculate_stage_duration(stage_since_str)
    
    # 判断推进状态
    if duration_days <= 7:
        status = "🟢 正常推进"
        urgency = "正常"
    elif duration_days <= 14:
        status = "🟡 进展放缓，建议加速"
        urgency = "重要"
    else:
        status = "🔴 进展缓慢，需要紧急干预"
        urgency = "紧急"
    
    # 生成下一步建议
    next_actions = generate_next_actions(stage, duration_days, customer)
    
    return {
        "customer_name": customer_name,
        "current_stage": stage,
        "stage_description": STAGES[stage],
        "duration_days": duration_days,
        "status": status,
        "urgency": urgency,
        "next_actions": next_actions,
        "conversion_rate": get_conversion_rate(stage),
        "estimated_closing_date": estimate_closing_date(stage, datetime.now()),
    }, None

def generate_next_actions(stage, duration_days, customer):
    """生成下一步行动建议"""
    actions = {"today": [], "tomorrow": [], "this_week": []}
    
    if stage == 1:  # 需求识别
        actions["today"] = ["发送园区介绍资料", "预约带看时间"]
        actions["tomorrow"] = ["电话跟进，确认需求细节"]
        actions["this_week"] = ["安排第一次带看"]
    
    elif stage == 2:  # 房源匹配
        actions["today"] = ["发送房源推荐方案", "确认带看时间"]
        actions["tomorrow"] = ["准备带看材料（园区介绍+政策）"]
        actions["this_week"] = ["执行带看", "发送带看总结"]
    
    elif stage == 3:  # 方案对比
        if duration_days > 7:
            actions["today"] = ["🟡 紧急：发送TCO成本对比报告", "强调我方优势（产业生态+政策支持）"]
            actions["tomorrow"] = ["🟡 预约第二次带看（看高区景观房源）"]
            actions["this_week"] = ["🟡 邀请决策人午餐会（建立高层关系）"]
        else:
            actions["today"] = ["发送TCO成本对比报告", "回答客户对比疑问"]
            actions["tomorrow"] = ["预约第二次带看"]
            actions["this_week"] = ["跟进决策进展"]
    
    elif stage == 4:  # 谈判
        actions["today"] = ["准备谈判要点（租金底线/租期/免租期）", "预约谈判会议"]
        actions["tomorrow"] = ["执行谈判", "记录谈判结果"]
        actions["this_week"] = ["根据谈判结果调整方案"]
    
    elif stage == 5:  # 决策
        actions["today"] = ["跟进内部决策进展", "提供补充材料（如需）"]
        actions["tomorrow"] = ["了解决策时间表"]
        actions["this_week"] = ["准备签约材料"]
    
    elif stage == 6:  # 签约
        actions["today"] = ["准备签约文件", "确认入驻时间"]
        actions["tomorrow"] = ["执行签约", "安排入驻事宜"]
        actions["this_week"] = ["完成入驻手续", "后续服务跟进"]
    
    return actions

def get_conversion_rate(stage):
    """获取阶段转化率（模拟数据）"""
    rates = {
        1: 85,  # 需求识别 → 房源匹配
        2: 75,  # 房源匹配 → 方案对比
        3: 65,  # 方案对比 → 谈判
        4: 80,  # 谈判 → 决策
        5: 90,  # 决策 → 签约
        6: 100, # 签约 → 成交
    }
    return rates.get(stage, 0)

def estimate_closing_date(stage, from_date):
    """预计成交时间"""
    days_to_close = {
        1: 60,  # 需求识别后约60天成交
        2: 45,  # 房源匹配后约45天成交
        3: 30,  # 方案对比后约30天成交
        4: 21,  # 谈判后约21天成交
        5: 14,  # 决策后约14天成交
        6: 7,   # 签约后约7天成交
    }
    
    days = days_to_close.get(stage, 30)
    closing_date = from_date + timedelta(days=days)
    return closing_date.strftime("%Y-%m-%d")

def format_stage_analysis(result):
    """格式化阶段分析报告"""
    output = f"# 📊 客户推进状态分析\n\n"
    
    output += f"## 客户信息\n"
    output += f"- **客户名称**：{result['customer_name']}\n"
    output += f"- **当前阶段**：阶段{result['current_stage']} - {result['stage_description']}\n"
    output += f"- **停留时间**：{result['duration_days']}天（建议≤7天）\n"
    output += f"- **推进状态**：{result['status']}\n"
    output += f"- **紧急程度**：{result['urgency']}\n\n"
    
    output += f"## 下一步行动建议\n"
    output += f"### 今日行动\n"
    for action in result['next_actions']['today']:
        output += f"- {action}\n"
    
    output += f"\n### 明日行动\n"
    for action in result['next_actions']['tomorrow']:
        output += f"- {action}\n"
    
    output += f"\n### 本周行动\n"
    for action in result['next_actions']['this_week']:
        output += f"- {action}\n"
    
    output += f"\n## 成交预测\n"
    output += f"- **阶段转化率**：{result['conversion_rate']}%（阶段{result['current_stage']}→阶段{result['current_stage']+1}）\n"
    output += f"- **预计成交时间**：{result['estimated_closing_date']}（未来{result['estimated_closing_date']}天）\n"
    
    output += f"\n## 阶段说明\n"
    for stage_id, stage_desc in STAGES.items():
        marker = "👉" if stage_id == result['current_stage'] else "  "
        output += f"{marker} 阶段{stage_id}：{stage_desc}\n"
    
    return output

def save_to_file(content, customer_name, output_dir=None):
    """保存分析报告到文件"""
    if output_dir is None:
        output_dir = os.path.expanduser("~/.workbuddy/workspace/investment-assistant")
    
    os.makedirs(output_dir, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y%m%d")
    output_file = os.path.join(output_dir, f"状态分析_{customer_name}_{date_str}.md")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
        f.write(f"\n\n---\n*本报告由招商助手自动生成 @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
    return output_file

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 judge_stage.py <客户名称>")
        print("示例: python3 judge_stage.py \"测试科技公司\"")
        sys.exit(1)
    
    customer_name = sys.argv[1]
    
    print(f"📊 开始分析客户阶段: {customer_name}")
    
    # 判断阶段
    result, error = judge_stage(customer_name)
    
    if error:
        print(error)
        sys.exit(1)
    
    # 格式化输出
    content = format_stage_analysis(result)
    print(content)
    
    # 保存文件
    output_file = save_to_file(content, customer_name)
    print(f"\n✅ 分析报告已保存: {output_file}")
    
    return output_file

if __name__ == "__main__":
    main()
