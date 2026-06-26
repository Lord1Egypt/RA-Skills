#!/usr/bin/env python3
"""
并购对接Skill - 辅助工具
功能：生成关键人画像卡、话术模板等

版本：v1.0
日期：2026年5月
"""

import os
from datetime import datetime
from typing import Dict, List, Optional

# ============================================================
# 配置区
# ============================================================

SKILL_NAME = "胡田-OPC导师-并购对接"
SKILL_VERSION = "v1.0"

# ============================================================
# 关键人类型定义
# ============================================================

KEY_PERSON_TYPES = {
    "secretary": {
        "name": "董秘",
        "influence_level": 3,
        "contact_difficulty": 2,
        "best_approach": "投资者/行业研究者身份",
        "entry_phase": "信息入口"
    },
    "executive": {
        "name": "高管层(CEO/CFO)",
        "influence_level": 5,
        "contact_difficulty": 4,
        "best_approach": "项目推介/中间人引荐",
        "entry_phase": "决策推动"
    },
    "controlling_shareholder": {
        "name": "大股东/实控人",
        "influence_level": 5,
        "contact_difficulty": 5,
        "best_approach": "中间人引荐",
        "entry_phase": "最终拍板"
    },
    "director": {
        "name": "独立董事/执行董事",
        "influence_level": 4,
        "contact_difficulty": 3,
        "best_approach": "学术会议/行业活动",
        "entry_phase": "意见影响"
    },
    "external_advisor": {
        "name": "外部顾问(FA/券商/律所)",
        "influence_level": 3,
        "contact_difficulty": 2,
        "best_approach": "行业活动/直接联系",
        "entry_phase": "催化剂"
    }
}

# ============================================================
# 接触策略路径
# ============================================================

APPROACH_PATHS = {
    "cold": {
        "name": "冷启动",
        "description": "无任何关系基础，需要从头建立联系",
        "channels": ["公开渠道触达", "活动接触", "信息影响"]
    },
    "warm": {
        "name": "温启动",
        "description": "有一度人脉，可以通过中间人引荐",
        "channels": ["中间人引荐", "借势搭车", "价值交换"]
    },
    "hot": {
        "name": "热启动",
        "description": "有强力背书人直接引荐",
        "channels": ["背书人直接带见", "背书人提前沟通", "高层对话"]
    }
}

# ============================================================
# 状态代码
# ============================================================

STATUS_CODES = {
    "S0": {"name": "待联系", "description": "尚未发起联系"},
    "S1": {"name": "跟进中", "description": "已联系，等待回复"},
    "S2": {"name": "深度沟通", "description": "进入深入交流阶段"},
    "S3": {"name": "尽调阶段", "description": "已进入尽调"},
    "S4": {"name": "暂停", "description": "暂时搁置"},
    "S5": {"name": "已放弃", "description": "已明确放弃"},
    "S6": {"name": "已签约", "description": "交易完成"}
}


# ============================================================
# 生成器函数
# ============================================================

def generate_key_person_profile(
    person_type: str,
    name: str = "",
    company: str = "",
    tenure: str = "",
    background: str = "",
    contact_difficulty: str = "",
    notes: str = ""
) -> str:
    """生成关键人画像卡"""
    
    if person_type not in KEY_PERSON_TYPES:
        return "错误：不支持的关键人类型"
    
    info = KEY_PERSON_TYPES[person_type]
    
    template = f"""
【关键人画像卡】

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

一、基本信息
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
姓名：{name or '待填写'}
职位：{info['name']}
公司：{company or '待填写'}
任期：{tenure or '待填写'}

二、背景信息
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【背景描述】
{background or '待填写'}

三、关键人特征
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
决策影响力：L{info['influence_level']} / L5
接触难度：{info['contact_difficulty']}星（5星最难）
最佳接触方式：{info['best_approach']}
介入阶段：{info['entry_phase']}

四、接触策略建议
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
推荐切入点：{notes or '待分析'}
关键话术：见话术库文档

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    return template


def generate_one_page_summary_template(
    company_name: str = "",
    founded_year: str = "",
    registered_capital: str = "",
    industry: str = "",
    core_tech: str = "",
    revenue: str = "",
    net_profit: str = "",
    growth_trend: str = "",
    patents: str = "",
    qualifications: str = "",
    cooperation_mode: str = "",
    expected_valuation: str = "",
    fund_usage: str = "",
    contact_name: str = "",
    contact_phone: str = "",
    contact_email: str = ""
) -> str:
    """生成一页纸项目摘要模板"""
    
    template = f"""
【项目摘要】

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[公司/项目名称] · 投资价值概览
{datetime.now().strftime('%Y年%m月')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【一句话介绍】
[用一句话描述项目核心价值，控制在20字以内]

【公司概况】
成立时间：{founded_year or '____年'}
注册资本：{registered_capital or '____万元'}
所在领域：{industry or '____行业'}
核心技术：{core_tech or '____技术'}

【核心亮点】（3-5个）
• 亮点1：[描述技术领先性或市场地位]
• 亮点2：[描述商业模式或客户资源]
• 亮点3：[描述团队背景或资质壁垒]

【财务概况】
• 营收：{revenue or '____万元'}（近一年）
• 净利润：{net_profit or '____万元'}（近一年）
• 增长趋势：{growth_trend or '同比增速+说明'}

【技术/资质壁垒】
• 专利：{patents or '__项（发明__项）'}
• 资质：{qualifications or '列出主要资质认证'}
• 技术领先性：[描述技术优势]

【合作需求】
• 合作模式：{cooperation_mode or '□并购  □战略投资  □业务合作'}
• 期望估值：{expected_valuation or '____万元'}
• 资金用途：{fund_usage or '简述主要用途'}

【联系方式】
联系人：{contact_name or '[姓名]'}
手机：{contact_phone or '[____]'}
邮箱：{contact_email or '[____]'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    return template


def generate_contact_strategy_report(
    company_name: str,
    approach_path: str,
    target_persons: List[str],
    contact_channels: List[str],
    key_messages: List[str]
) -> str:
    """生成接触策略报告"""
    
    if approach_path not in APPROACH_PATHS:
        return "错误：不支持的接触路径"
    
    path_info = APPROACH_PATHS[approach_path]
    
    template = f"""
【接触策略报告】

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

一、目标公司
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
公司名称：{company_name}
接触路径：{path_info['name']}
路径说明：{path_info['description']}

二、推荐接触方式
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    for i, channel in enumerate(path_info['channels'], 1):
        template += f"{i}. {channel}\n"
    
    template += f"""
三、目标关键人
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    for person in target_persons:
        person_type = KEY_PERSON_TYPES.get(person, {})
        template += f"• {person_type.get('name', person)} - 影响力L{person_type.get('influence_level', '?')}\n"
    
    template += f"""
四、推荐渠道
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    for channel in contact_channels:
        template += f"• {channel}\n"
    
    template += f"""
五、关键信息要点
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    for msg in key_messages:
        template += f"• {msg}\n"
    
    template += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return template


def generate_progress_tracker_template() -> str:
    """生成进度追踪模板"""
    
    template = """
【并购对接进度追踪表】

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| 公司 | 联系人 | 状态 | 最后联系 | 下次跟进 | 优先级 |
|------|--------|------|----------|----------|--------|
| [公司A] | [姓名] | S2 | 5月10日 | 5月17日 | P1 |
| [公司B] | [姓名] | S1 | 5月8日 | 5月15日 | P2 |
| [公司C] | [姓名] | S3 | 5月5日 | 5月12日 | P1 |
| [公司D] | [姓名] | S0 | - | 5月20日 | P3 |
| [公司E] | [姓名] | S4 | 4月20日 | 6月20日 | P2 |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

状态代码说明：
"""
    
    for code, info in STATUS_CODES.items():
        template += f"• {code} {info['name']}：{info['description']}\n"
    
    template += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return template


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数 - 演示生成功能"""
    
    print("=" * 60)
    print(f"{SKILL_NAME} v{SKILL_VERSION}")
    print("=" * 60)
    print()
    
    # 示例1：生成董秘画像
    print("【示例1：生成董秘画像卡】")
    print(generate_key_person_profile(
        person_type="secretary",
        name="张三",
        company="XX上市公司",
        tenure="2020年至今",
        background="毕业于XX大学，曾在XX券商投行部任职",
        notes="倾向于开放型沟通，关注新技术领域"
    ))
    
    # 示例2：生成一页纸摘要
    print("\n【示例2：生成一页纸摘要模板】")
    print(generate_one_page_summary_template(
        company_name="智联传感",
        founded_year="2019",
        registered_capital="1,000",
        industry="智能制造-工业传感器",
        core_tech="MEMS高精度压力传感器",
        revenue="2,800万元",
        net_profit="420万元"
    ))
    
    # 示例3：生成接触策略
    print("\n【示例3：生成接触策略报告】")
    print(generate_contact_strategy_report(
        company_name="宁德时代",
        approach_path="cold",
        target_persons=["secretary", "executive"],
        contact_channels=["年报披露的董秘邮箱", "官网投资者关系页面"],
        key_messages=[
            "我们是做固态电池技术的",
            "技术处于行业领先地位",
            "寻求技术合作或并购机会"
        ]
    ))
    
    # 示例4：生成进度追踪表
    print("\n【示例4：生成进度追踪表】")
    print(generate_progress_tracker_template())


if __name__ == "__main__":
    main()
