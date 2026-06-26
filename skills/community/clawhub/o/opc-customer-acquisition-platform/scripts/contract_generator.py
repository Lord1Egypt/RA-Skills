#!/usr/bin/env python3
"""
合约文档自动生成脚本
功能：根据项目信息自动生成合约文档
"""

import os
from datetime import datetime

# 模板文件路径
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'contracts')

# 输出目录
OUTPUT_DIR = './output'

def ensure_dir(path):
    """确保目录存在"""
    if not os.path.exists(path):
        os.makedirs(path)

def generate_project_id():
    """生成项目编号"""
    return f"OPC-PJ-{datetime.now().year}-{datetime.now().strftime('%m%d%H%M')}"

def generate_protocol_number(project_id, suffix='XY'):
    """生成协议编号"""
    return f"{project_id}-{suffix}"

def generate_contract(contract_type, project_info):
    """
    生成合约文档
    
    参数:
        contract_type: 合约类型
            - project_release: 项目发布单
            - bid_submission: 竞标书
            - bid_evaluation: 评标打分表
            - subcontract: 分包协议
            - spv_agreement: SPV合作协议
            - nda: 保密协议
            - quality_commitment: 质量承诺书
            - milestone_acceptance: 里程碑验收表
            - distribution_confirm: 分账确认书
            - project_closing: 项目结项报告
            - mutual_evaluation: 互评表
        project_info: 项目信息字典
    """
    
    project_id = generate_project_id()
    
    generators = {
        'project_release': generate_project_release,
        'bid_submission': generate_bid_submission,
        'bid_evaluation': generate_bid_evaluation,
        'subcontract': generate_subcontract,
        'spv_agreement': generate_spv_agreement,
        'nda': generate_nda,
        'quality_commitment': generate_quality_commitment,
        'milestone_acceptance': generate_milestone_acceptance,
        'distribution_confirm': generate_distribution_confirm,
        'project_closing': generate_project_closing,
        'mutual_evaluation': generate_mutual_evaluation,
    }
    
    if contract_type not in generators:
        raise ValueError(f"未知的合约类型: {contract_type}")
    
    return generators[contract_type](project_id, project_info)

def generate_project_release(project_id, info):
    """生成项目发布单"""
    content = f"""# 项目发布单

**项目编号**：{project_id}
**发布日期**：{datetime.now().strftime('%Y年%m月%d日')}
**发布方**：{info.get('publisher', '________________')}
**发布人**：{info.get('publisher_name', '________________')}  **联系方式**：________________

---

## 一、项目基本信息

| 项目 | 内容 |
|------|------|
| **项目名称** | {info.get('project_name', '________________________')} |
| **项目类型** | □设计类  □开发类  □营销类  □咨询类  □内容类  □其他 |
| **项目分级** | □D级  □C级  □B级  □A级  □S级 |

## 二、项目需求

**需求描述**：{info.get('description', '[详细描述项目需求]')}

**交付物清单**：
| 序号 | 交付物名称 | 数量 | 格式要求 |
|------|-----------|------|----------|
| 1 | {info.get('deliverable_1', '|')} | | |
| 2 | {info.get('deliverable_2', '|')} | | |

**质量标准**：{info.get('quality_standard', '[描述验收标准]')}

## 三、项目参数

| 项目 | 内容 |
|------|------|
| **项目金额** | 人民币 {info.get('budget', '[____]')} 元 |
| **项目周期** | {info.get('周期', '[__]')} 天/周 |
| **开始时间** | {datetime.now().strftime('%Y年%m月%d日')} |
| **截止时间** | {info.get('end_date', '____年__月__日')} |

## 四、技能要求

{info.get('skills', '□ 技能1 □ 技能2 □ 技能3')}

---

**发布人签字**：________________  **日期**：________________
**平台审核签字**：________________  **日期**：________________
"""
    return content

def generate_bid_submission(project_id, info):
    """生成竞标书"""
    return f"""# 竞标书

**项目名称**：{info.get('project_name', '________________')}
**项目编号**：{project_id}
**竞标方**：{info.get('bidder_name', '________________')}
**竞标日期**：{datetime.now().strftime('%Y年%m月%d日')}

---

## 一、公司/团队介绍

{info.get('company_intro', '[公司/团队介绍]')}

## 二、执行方案

{info.get('solution', '[执行方案]')}

## 三、报价方案

**总报价**：人民币大写 {info.get('price', '[________________]')} 元（¥{info.get('price_amount', '[____]')}元）

## 四、时间承诺

**承诺工期**：{info.get('timeline', '[__]')}天

---

**竞标方签字/盖章**：________________
**日期**：{datetime.now().strftime('%Y年%m月%d日')}
"""

def generate_bid_evaluation(project_id, info):
    """生成评标打分表"""
    bidders = info.get('bidders', [])
    table_rows = ""
    for i, bidder in enumerate(bidders):
        table_rows += f"| 竞标方{i+1} | {bidder.get('credit_level', '|')} | | | | |\n"
    
    return f"""# 评标打分表

**项目名称**：{info.get('project_name', '________________')}
**项目编号**：{project_id}
**评标日期**：{datetime.now().strftime('%Y年%m月%d日')}

---

## 竞标方基本信息

| 竞标方 | 信用等级 | 历史项目数 | 平均好评率 | 报名时间 |
|--------|---------|-----------|-----------|---------|
{table_rows}

## 综合得分汇总

| 竞标方 | 信用30 | 业绩25 | 方案25 | 报价15 | 时间5 | **总分100** | 排名 |
|--------|-------|-------|-------|-------|-------|-------------|------|
{table_rows}

---

## 评标结果

**推荐挂帅人**：________________
**推荐理由**：____________________________________________

评委签字：
"""
    return content

def generate_subcontract(project_id, info):
    """生成分包协议"""
    return f"""# 分包协议

**主项目编号**：{project_id}
**分包编号**：{project_id}-FB001
**甲方（挂帅人）**：{info.get('party_a', '________________')}
**乙方（接包人）**：{info.get('party_b', '________________')}
**签订日期**：{datetime.now().strftime('%Y年%m月%d日')}

---

## 一、分包项目信息

| 项目 | 内容 |
|------|------|
| **分包金额** | 人民币 {info.get('amount', '[____]')} 元 |
| **分包工期** | {info.get('timeline', '[__]')} 天 |

## 二、交付物清单

| 序号 | 交付物名称 | 交付时间 | 验收标准 |
|------|-----------|---------|---------|
| 1 | | | |

## 三、分账比例

甲方分账比例：{info.get('party_a_ratio', '[__]')}%
乙方分账比例：{info.get('party_b_ratio', '[__]')}%
"""
    return content

def generate_spv_agreement(project_id, info):
    """生成SPV合作协议"""
    members = info.get('members', [])
    member_rows = ""
    for i, member in enumerate(members):
        role = '甲方' if i == 0 else '乙方' if i == 1 else '丙方' if i == 2 else '丁方'
        member_rows += f"""### {role}：{member.get('name', '成员' + str(i+1))}

- **姓名/名称**：{member.get('name', '[_____]')}
- **联系方式**：{member.get('contact', '[_____]')}
- **分账比例**：{member.get('ratio', '[__]')}%

"""
    
    return f"""# SPV项目合作协议（获客分包版）

**协议编号**：{project_id}
**版本**：V1.0
**签署日期**：{datetime.now().strftime('%Y年%m月%d日')}

---

## 项目基本信息

| 项目 | 内容 |
|------|------|
| **项目名称** | {info.get('project_name', '________________')} |
| **项目金额** | 人民币 {info.get('budget', '[____]')} 元 |
| **项目周期** | {info.get('timeline', '[__]')} 天/月 |

## 协议各方

{member_rows}

---

## 分账比例

| 贡献者 | 分账比例 |
|--------|----------|
""" + "|".join([f"{m.get('name', '成员'+str(i+1))} | {m.get('ratio', '[__]')}% |" for i, m in enumerate(members)]) + """
"""
    return content

def generate_nda(project_id, info):
    """生成保密协议"""
    return f"""# 保密协议

**协议编号**：{project_id}-ND
**项目名称**：{info.get('project_name', '________________')}
**签署日期**：{datetime.now().strftime('%Y年%m月%d日')}

---

## 协议各方

**甲方（信息提供方）**：{info.get('party_a', '________________')}
**乙方（信息接收方）**：{info.get('party_b', '________________')}

## 保密期限

本协议自签署之日起生效，保密义务有效期为 **2年**。

## 违约责任

违反本协议，应支付违约金 **人民币 {info.get('penalty', '[____]')} 元**。

---

甲方：________________  乙方：________________  日期：{datetime.now().strftime('%Y年%m月%d日')}
"""
    return content

def generate_quality_commitment(project_id, info):
    """生成质量承诺书"""
    return f"""# 质量承诺书

**协议编号**：{project_id}-ZL
**项目名称**：{info.get('project_name', '________________')}
**签署日期**：{datetime.now().strftime('%Y年%m月%d日')}

---

## 承诺方信息

**承诺方**：{info.get('party', '________________')}
**负责模块**：{info.get('module', '________________')}

## 质量承诺

1. 按时交付符合标准的交付物
2. 交付物质量满足验收要求
3. 及时响应反馈，整改到位

## 违约责任

| 违约情形 | 违约责任 |
|----------|----------|
| 质量不达标 | 免费整改至达标 |
| 延期交付 | 每延期1天支付合同金额的0.5% |

---

承诺人：________________  日期：{datetime.now().strftime('%Y年%m月%d日')}
"""
    return content

def generate_milestone_acceptance(project_id, info):
    """生成里程碑验收表"""
    milestones = info.get('milestones', [])
    rows = ""
    for i, m in enumerate(milestones):
        rows += f"""### 里程碑 M{i}：{m.get('name', '阶段' + str(i))}

| 项目 | 内容 |
|------|------|
| **计划时间** | {m.get('date', '____年__月__日')} |
| **分账金额** | {m.get('amount', '[____]')} 元 |

#### 交付物

| 序号 | 交付物 | 状态 |
|------|--------|------|
| 1 | | □已交付 □未交付 |

#### 验收记录

| 项目 | 内容 |
|------|------|
| **验收结论** | □通过 □不通过 |
| **验收人** | ________________ |

"""
    
    return f"""# 里程碑验收表

**项目名称**：{info.get('project_name', '________________')}
**项目编号**：{project_id}

---

{rows}

## 最终验收

| 项目 | 内容 |
|------|------|
| **整体验收** | □通过 □不通过 |
| **验收人（客户）** | ________________ |
| **验收日期** | {datetime.now().strftime('%Y年%m月%d日')} |
"""
    return content

def generate_distribution_confirm(project_id, info):
    """生成分账确认书"""
    members = info.get('members', [])
    rows = ""
    for i, m in enumerate(members):
        rows += f"| {i+1} | {m.get('name', '成员'+str(i+1))} | | | {m.get('amount', '[____]')} 元 |\n"
    
    return f"""# 分账确认书

**协议编号**：{project_id}-FZ
**项目名称**：{info.get('project_name', '________________')}
**分账日期**：{datetime.now().strftime('%Y年%m月%d日')}

---

## 分账计算

| 项目 | 金额 |
|------|------|
| 项目到账金额 | {info.get('received_amount', '[____]')} 元 |
| 预留税费（10%） | {info.get('tax', '[____]')} 元 |
| 平台服务费（5%） | {info.get('platform_fee', '[____]')} 元 |
| 可分配金额 | {info.get('distributable', '[____]')} 元 |

## 分账明细

| 序号 | 参与方 | 开户行 | 账户名 | 分账金额 |
|------|--------|--------|--------|----------|
{rows}

## 各方确认

| 序号 | 参与方 | 确认金额 | 签字 | 日期 |
|------|--------|----------|------|------|
""" + "|".join([f" | {i+1} | {m.get('name', '成员'+str(i+1))} | {m.get('amount', '[____]')} 元 | ________________ | |\n" for i, m in enumerate(members)])
    return content

def generate_project_closing(project_id, info):
    """生成项目结项报告"""
    return f"""# 项目结项报告

**项目名称**：{info.get('project_name', '________________')}
**项目编号**：{project_id}
**结项日期**：{datetime.now().strftime('%Y年%m月%d日')}

---

## 项目基本信息

| 项目 | 内容 |
|------|------|
| **项目金额** | {info.get('budget', '[____]')} 元 |
| **项目周期** | {info.get('timeline', '[__]')} 天 |
| **挂帅人** | {info.get('leader', '________________')} |

## 目标达成

{info.get('goal_status', '[描述目标达成情况]')}

## 经验教训

{info.get('lessons', '[总结经验教训]')}

---

## 结项确认

| 角色 | 姓名 | 签字 | 日期 |
|------|------|------|------|
| **挂帅人** | | ________________ | |
| **客户代表** | | ________________ | |
"""
    return content

def generate_mutual_evaluation(project_id, info):
    """生成互评表"""
    return f"""# 互评表

**项目名称**：{info.get('project_name', '________________')}
**项目编号**：{project_id}
**评价日期**：{datetime.now().strftime('%Y年%m月%d日')}

---

## 甲方评价乙方

| 评价维度 | 权重 | 评分(1-5) |
|----------|------|-----------|
| 交付质量 | 25% | |
| 时效性 | 25% | |
| 专业能力 | 20% | |
| 沟通协作 | 15% | |
| 服务态度 | 15% | |

**综合评价**：□非常满意 □满意 □一般 □不满意

## 乙方评价甲方

| 评价维度 | 权重 | 评分(1-5) |
|----------|------|-----------|
| 配合程度 | 30% | |
| 需求清晰度 | 25% | |
| 付款及时性 | 25% | |
| 沟通效率 | 20% | |

---

## 双方签字

| 角色 | 姓名 | 签字 | 日期 |
|------|------|------|------|
| **甲方评价人** | | ________________ | |
| **乙方评价人** | | ________________ | |
"""
    return content

def save_contract(content, contract_type, project_id):
    """保存合约文档"""
    ensure_dir(OUTPUT_DIR)
    filename = f"{OUTPUT_DIR}/{project_id}_{contract_type}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return filename

# 示例使用
if __name__ == "__main__":
    # 示例项目信息
    project_info = {
        'project_name': '企业官网开发项目',
        'publisher': 'XX科技有限公司',
        'publisher_name': '张三',
        'budget': '80,000',
        'timeline': '30',
        'description': '开发一套企业官网，包含首页、关于我们、产品展示、新闻动态、联系我们等模块。',
        'deliverable_1': '前端页面（HTML/CSS/JS）',
        'deliverable_2': '后台管理系统',
        'quality_standard': '响应式设计，兼容主流浏览器，加载速度<3秒',
        'members': [
            {'name': '李四', 'contact': '13800138000', 'ratio': '40'},
            {'name': '王五', 'contact': '13900139000', 'ratio': '35'},
            {'name': '赵六', 'contact': '13700137000', 'ratio': '25'},
        ],
        'bidders': [
            {'name': '竞标方A', 'credit_level': 'A'},
            {'name': '竞标方B', 'credit_level': 'B'},
        ],
        'milestones': [
            {'name': '需求确认', 'date': '2026-06-01', 'amount': '20,000'},
            {'name': '开发完成', 'date': '2026-06-20', 'amount': '40,000'},
            {'name': '验收通过', 'date': '2026-06-30', 'amount': '20,000'},
        ]
    }
    
    # 生成所有合约
    for contract_type in ['project_release', 'spv_agreement', 'nda', 'quality_commitment']:
        try:
            content = generate_contract(contract_type, project_info)
            filename = save_contract(content, contract_type, project_info)
            print(f"已生成: {filename}")
        except Exception as e:
            print(f"生成{contract_type}失败: {e}")
