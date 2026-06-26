---
name: Insurance Knowledge Q&A Expert
slug: insurance-knowledge-qa
description: AI-powered insurance knowledge Q&A expert — covers insurance terminology explanation, product comparison, coverage analysis, and decision support for insurance buyers and agents. Built for China insurance consumers and professionals. Keywords: insurance knowledge, FAQ, product comparison, coverage analysis, insurance terminology, China insurance, 保险知识, 问答, 产品对比, 保障分析, 保险术语, 保险科普, 条款解读, 核保知识, 理赔知识, 险种对比, 健康告知.
version: "3.0.1"
---

# Insurance Knowledge Q&A Expert / 保险知识问答专家


### 保险监管最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| 保险监管 | 2026年4月保险新规全量知识更新：车险/人身险/医疗险三大领域 | 知识库需新增300+条2026年新规相关QA条目 |
| 保险监管 | 产品分级制度(P1-P5)、销售人员分级制度（一级至四级） | 知识库需新增300+条2026年新规相关QA条目 |
| 保险监管 | 慢特病目录62种、交强险保额42.2万、演示利率3.5% | 知识库需新增300+条2026年新规相关QA条目 |

> **数据截止**: 2026-05-25 | 来源：国家金融监督管理总局、安永Q1分析、行业公开信息
> **声明**: 以上动态供参考，具体以官方最新发布为准

> **English:** AI-powered insurance knowledge Q&A — covers terminology, product comparison, coverage analysis, and decision support.
>
> **中文:** 保险知识问答专家——覆盖保险术语、产品对比、保障分析、决策支持。

---

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 |
|------------------|-------------|------------------------|
| **术语复杂** | 保险条款晦涩难懂 | 通俗化术语解释 |
| **产品选择难** | 保险种类繁多，不知如何选 | 科学对比框架 |
| **保障不清晰** | 不知道保什么、不保什么 | 保障范围分析 |
| **代理人不专业** | 误导销售普遍存在 | 中立知识科普 |

---

## Trigger Keywords / 触发关键词

**English Triggers:** insurance knowledge, FAQ, product comparison, coverage analysis, insurance terminology, insurance buying guide

**中文触发词（优先）：** 保险知识 / 保险问答 / 保险术语 / 险种区别 / 重疾险 / 医疗险 / 寿险 / 意外险 / 理财险 / 保障分析 / 产品对比 / 怎么选 / 哪个好 / 是什么意思 / 条款解读 / 保险科普 / 保险小白 / 保险避坑

---

## Core Capabilities / 核心能力

### 1. Insurance Terminology / 保险术语库

```python
INSURANCE_GLOSSARY = {
    # 基础术语
    "投保人": {
        "definition": "与保险公司签订保险合同，缴纳保费的人",
        "example": "张三给儿子投保，张三就是投保人",
        "related_terms": ["被保险人", "受益人"],
        "mistakes": "很多人误以为投保人就是被保险人，实际上可以不同"
    },
    
    "被保险人": {
        "definition": "享受保险保障的人，即保险合同保障的对象",
        "example": "张三给儿子投保，儿子是被保险人",
        "related_terms": ["投保人", "受益人"]
    },
    
    "受益人": {
        "definition": "领取保险金的人，可以指定或法定",
        "example": "重疾险受益人通常是被保险人本人；寿险受益人可以指定",
        "types": {
            "指定受益人": "合同中明确指定的人",
            "法定受益人": "按继承法规定的顺序继承人"
        }
    },
    
    "保费": {
        "definition": "投保人为获得保险保障需要缴纳的费用",
        "types": {
            "趸交": "一次性缴清全部保费",
            "期交": "按年/半年/季度/月缴纳",
            "自然保费": "随风险变化调整的保费",
            "均衡保费": "每年固定金额的保费"
        }
    },
    
    "保额": {
        "definition": "保险公司承担赔偿或给付的最高限额",
        "example": "投保50万重疾险，保额就是50万",
        "tips": "保额要足够覆盖风险损失，一般建议重疾险为3-5年年收入"
    },
    
    # 产品类型术语
    "等待期": {
        "definition": "保险合同生效后的一段时间内，保险公司不承担给付责任",
        "common_periods": {
            "重疾险": "90天或180天",
            "医疗险": "30天",
            "寿险": "通常无等待期",
            "意外险": "通常无等待期"
        },
        "reason": "防止带病投保，保护保险公司和其他投保人利益"
    },
    
    "犹豫期": {
        "definition": "投保后可以无条件退保的时间，通常为15天",
        "calculation": "自签收合同次日起15天内",
        "fees": "犹豫期内退保，扣除不超过10元工本费后返还保费",
        "tips": "收到合同后要仔细阅读，有问题及时退保"
    },
    
    "宽限期": {
        "definition": "保费到期未缴，保险公司给予的补缴期限，通常为60天",
        "protection": "宽限期内出险，保险公司仍承担给付责任，但会扣除欠缴保费",
        "lapse": "超过60天未缴，保单效力中止"
    },
    
    # 理赔相关
    "免赔额": {
        "definition": "保险公司不负责赔偿的费用，由被保险人自行承担",
        "types": {
            "绝对免赔额": "低于免赔额的部分完全不赔",
            "相对免赔额": "低于免赔额的部分不赔，超过的部分全赔"
        },
        "example": "免赔额1万，医疗费3万，则保险公司赔付2万"
    },
    
    "给付方式": {
        "types": {
            "报销型": "花费多少报销多少，不能重复理赔（如医疗险）",
            "定额给付型": "达到约定条件一次性给付（如重疾险）",
            "津贴型": "按住院天数等标准给付（如住院津贴）"
        }
    }
}
```

### 2. Product Comparison Framework / 产品对比框架

```python
PRODUCT_COMPARISON = {
    "重疾险对比表": {
        "dimensions": [
            "保障范围",
            "赔付次数",
            "赔付比例",
            "保费价格",
            "等待期",
            "健康告知",
            "附加服务"
        ],
        "example_brands": {
            "A公司": {
                "保障病种": "120种重疾+40种轻症",
                "重疾赔付": "1次",
                "轻症赔付": "3次，每次30%",
                "等待期": "180天",
                "特点": "大品牌，网点多"
            },
            "B公司": {
                "保障病种": "110种重疾+50种轻症+25种中症",
                "重疾赔付": "分组多次赔付",
                "轻症赔付": "不分组多次赔付",
                "等待期": "90天",
                "特点": "轻症/中症保障更全面"
            },
            "C公司": {
                "保障病种": "100种重疾+30种轻症",
                "重疾赔付": "单次赔付",
                "轻症赔付": "3次，每次20%",
                "等待期": "90天",
                "特点": "价格便宜，性价比高"
            }
        }
    },
    
    "医疗险对比表": {
        "dimensions": [
            "保障额度",
            "报销比例",
            "免赔额",
            "报销范围",
            "续保条件",
            "增值服务"
        ],
        "example_types": {
            "百万医疗": {
                "额度": "200-600万",
                "比例": "100%（经社保）",
                "免赔额": "1万",
                "范围": "二级及以上公立医院普通部",
                "续保": "不保证续保/保证续保6年",
                "适合": "大额医疗风险防范"
            },
            "中端医疗": {
                "额度": "20-200万",
                "比例": "100%",
                "免赔额": "可选0",
                "范围": "含特需/国际部",
                "续保": "通常不保证续保",
                "适合": "提升就医体验"
            },
            "高端医疗": {
                "额度": "无上限",
                "比例": "100%",
                "免赔额": "可选",
                "范围": "全球/私立医院/孕产/齿科",
                "续保": "优客计划",
                "适合": "高端医疗资源"
            }
        }
    }
}
```

### 3. Coverage Analysis / 保障分析

```markdown
## 家庭保障配置分析框架

### 保障缺口计算

```python
def calculate_protection_gap(family_profile: dict) -> dict:
    """
    计算家庭保障缺口
    """
    # 风险损失 = 收入损失 + 债务 + 费用 - 已有保障
    income_loss = family_profile["annual_income"] * family_profile["income_years"]
    debt = family_profile["mortgage"] + family_profile["other_debt"]
    expenses = family_profile["children_education"] + family_profile["elderly_support"]
    existing = family_profile["existing_coverage"]
    
    # 各险种缺口
    gaps = {
        "寿险缺口": max(0, income_loss + debt + expenses - existing.get("寿险", 0)),
        "重疾险缺口": max(0, income_loss * 0.5 + expenses - existing.get("重疾险", 0)),
        "医疗险缺口": max(0, family_profile["medical_risk"] - existing.get("医疗险", 0)),
        "意外险缺口": max(0, income_loss * 2 - existing.get("意外险", 0))
    }
    
    return gaps
```

### 家庭配置方案模板

| 成员 | 险种 | 建议保额 | 保障重点 |
|-----|------|---------|---------|
| 家庭支柱 | 寿险 | 10年年收入+负债 | 身故/全残 |
| 家庭支柱 | 重疾险 | 3-5年年收入 | 重疾保障 |
| 家庭支柱 | 医疗险 | 200万+ | 大额医疗 |
| 家庭支柱 | 意外险 | 5-10倍年收入 | 意外身故/伤残 |
| 配偶 | 重疾险 | 3年年收入 | 重疾保障 |
| 配偶 | 医疗险 | 200万+ | 大额医疗 |
| 配偶 | 意外险 | 3-5倍年收入 | 意外保障 |
| 孩子 | 重疾险 | 50万+ | 少儿特定疾病 |
| 孩子 | 医疗险 | 200万+ | 住院医疗 |
| 孩子 | 意外险 | 20-50万 | 意外医疗 |
| 老人 | 医疗险/防癌险 | 200万+/10-20万 | 大病保障 |
| 老人 | 意外险 | 10-20万 | 意外医疗/骨折 |
```

### 避坑指南

```markdown
## 常见保险误区

### ❌ 误区1：买保险先给孩子买
**正确**：先保大人，后保孩子
**原因**：大人是家庭经济支柱，大人出事孩子无人照顾

### ❌ 误区2：买返还型保险更划算
**正确**：看保障是否足够，不要为了返本牺牲保额
**原因**：返还型保费贵，相同预算下保额低

### ❌ 误区3：买一份保险保所有
**正确**：不同险种功能不同，不要用医疗险当重疾险用
**原因**：保障重叠或缺失都无法有效转移风险

### ❌ 误区4：健康告知不重要
**正确**：如实告知，避免理赔纠纷
**原因**：未如实告知可能导致拒赔

### ❌ 误区5：保险可以等有钱再买
**正确**：越早买越便宜，保障越早越好
**原因**：年龄越大保费越高，身体变化可能影响投保
```
```

---

## Quick Command Templates / 快速指令模板

**术语查询：**
```
解释保险术语"等待期"
```

**产品对比：**
```
对比医疗险：百万医疗、中端医疗、高端医疗的区别
```

**配置建议：**
```
给家庭配置保险：
- 先生35岁，年收入30万，有房贷200万
- 太太33岁，年收入15万
- 孩子5岁
- 已有保障：各自1份重疾险50万
```

---

## Disclaimer

This skill provides insurance knowledge for educational purposes only. Insurance decisions should be made based on individual circumstances and professional advice. This skill does not constitute insurance sales or solicitation.
