---
name: Insurance Intelligent Customer Service System
slug: insurance-customer-service
description: AI-powered insurance intelligent customer service — covers policy inquiry, claims guidance, product consultation, renewal reminders, and PIPL-compliant data handling. Built for China life and property insurance companies. Keywords: insurance customer service, policy inquiry, claims guidance, PIPL compliance, China insurance, 保险客服, 理赔咨询, 保单查询, 续期提醒, 智能客服, 保险话术, FAQ, 智能问答, 机器人客服, 24小时客服, 呼入客服.
version: "3.0.1"
---

# Insurance Intelligent Customer Service System / 保险智能客服系统


### 保险监管最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| 保险监管 | 2026年4月新规：智能客服需支持产品分级(P1-P5)告知和风险测评引导 | 知识库和FAQ需全面覆盖2026年新规内容 |
| 保险监管 | 合规管理深化：所有线上客服对话需满足合规留存要求 | 知识库和FAQ需全面覆盖2026年新规内容 |
| 保险监管 | 车险/医疗险新规知识库更新（交强险保额/慢特病/异地就医等） | 知识库和FAQ需全面覆盖2026年新规内容 |

> **数据截止**: 2026-05-25 | 来源：国家金融监督管理总局、安永Q1分析、行业公开信息
> **声明**: 以上动态供参考，具体以官方最新发布为准

> **English:** AI-powered insurance customer service — covers policy inquiry, claims guidance, product consultation, and PIPL-compliant data handling.
>
> **中文:** 保险智能客服——覆盖保单查询、理赔指导、产品咨询、续期提醒、PIPL合规数据处理。

---

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 |
|------------------|-------------|------------------------|
| **理赔流程复杂** | 客户不清楚理赔步骤 | 智能理赔引导 |
| **等待时间长** | 人工客服繁忙 | AI秒级响应 |
| **条款难懂** | 健康告知/免责条款复杂 | 通俗化解读 |
| **续期提醒** | 客户忘记续费导致失效 | 自动续期提醒 |
| **PIPL合规** | 客户信息处理合规要求 | 合规数据处理框架 |

---

## Trigger Keywords / 触发关键词

**English Triggers:** insurance customer service, policy inquiry, claims guidance, PIPL compliance, China insurance, policy renewal, insurance consultation

**中文触发词（优先）：** 保险客服 / 理赔咨询 / 保单查询 / 续期提醒 / 产品咨询 / 健康告知 / 免责条款 / 核保 / 保全 / 保全变更 / 保单贷款 / 退保 / 犹豫期 / 等待期 / 出险 / 报案 / 理赔材料 / 保险术语

---

## Core Capabilities / 核心能力

### 1. Policy Inquiry / 保单查询

```python
POLICY_INQUIRY_FLOWS = {
    "保单基本信息查询": {
        "steps": [
            "身份验证（姓名+身份证+手机号验证）",
            "选择要查询的保单",
            "展示保单基本信息"
        ],
        "response_template": """
        您好，您的保单信息如下：
        
        【保单号】：{policy_no}
        【产品名称】：{product_name}
        【保险公司】：{company_name}
        【投保人】：{policy_holder}
        【被保险人】：{insured}
        【生效日期】：{start_date}
        【到期日期】：{end_date}
        【保额】：{coverage_amount}元
        【年缴保费】：{annual_premium}元
        【缴费方式】：{payment_method}
        【当前状态】：{status}
        
        如需了解更多信息，请告诉我：
        - 理赔信息
        - 保全变更
        - 续期缴费
        """
    },
    
    "理赔进度查询": {
        "steps": [
            "报案号验证",
            "身份核验",
            "展示理赔进度"
        ],
        "status_levels": {
            "submitted": "已提交材料，待审核",
            "under_review": "审核中，预计3个工作日完成",
            "survey_scheduled": "已安排查勘，请保持电话畅通",
            "survey_completed": "查勘完成，审核中",
            "approved": "审核通过，理赔款处理中",
            "paid": "理赔款已到账",
            "rejected": "审核不通过，原因：{rejection_reason}"
        }
    }
}
```

### 2. Claims Guidance / 理赔指导

```markdown
## 理赔智能引导

### 理赔类型判断流程

```
客户描述 → AI识别 → 理赔类型 → 材料清单 → 报案指引
```

### 各险种理赔材料清单

| 险种类型 | 必需材料 | 可选材料 | 特殊要求 |
|---------|---------|---------|---------|
| **医疗险** | 发票原件、费用清单、出院小结、身份证 | 病历、社保结算单 | 需医院盖章 |
| **重疾险** | 诊断证明（含病理报告）、身份证 | 病历、手术记录 | 需确诊符合条款定义 |
| **寿险** | 死亡证明、户籍注销证明、受益人身份证 | 事故证明、调查报告 | 指定受益人需提供关系证明 |
| **意外险** | 意外事故证明、医疗票据、身份证 | 警方报告、工伤认定 | 需证明属于意外 |
| **车险** | 事故认定书、车辆照片、维修发票 | 责任认定、保险单 | 人伤需提供伤情证明 |

### 理赔时效参考

| 理赔金额 | 正常时效 | 加急条件 |
|---------|---------|---------|
| <5000元 | 3个工作日 | 无 |
| 5000-1万元 | 5个工作日 | 资料完整 |
| 1万-10万元 | 7个工作日 | 无需调查 |
| >10万元 | 10-15个工作日 | 需调查 |
```

### AI智能报案话术

```python
CLAIMS_REPORTING_SCRIPT = {
    "开场": """
    "您好，这里是{保险公司}客服热线，
    我是智能客服小保，请问有什么可以帮您？
    
    听您说想要报案，请不要着急，
    我来帮您一步一步完成报案操作。"
    """,
    
    "信息收集": """
    "为了帮您顺利完成报案，请提供以下信息：
    
    1. 被保险人姓名：{name}
    2. 保单号码：{policy_no}
    3. 出险时间：{accident_date}
    4. 出险原因：{accident_cause}
    5. 简要描述事故经过：{description}
    6. 预计理赔金额：{estimated_amount}
    
    请放心，您提供的信息我们会严格保密，仅用于理赔处理。"
    """,
    
    "报案确认": """
    "好的，我已经记录了您的报案信息：
    
    【报案编号】：{report_no}
    【被保险人】：{name}
    【出险时间】：{accident_date}
    【出险原因】：{accident_cause}
    【预计理赔金额】：{estimated_amount}
    
    下一步请准备以下理赔材料：
    {material_list}
    
    材料准备好后，您可以通过以下方式提交：
    1. {method_1}
    2. {method_2}
    3. {method_3}
    
    提交后，预计{time}个工作日内完成审核。
    
    请问还有其他问题吗？"
    """
}
```

### 3. PIPL Compliance Framework / PIPL合规框架

```markdown
## PIPL合规数据处理规范

### 客服对话数据处理原则

| 原则 | 说明 | 实施措施 |
|-----|------|---------|
| **最小必要** | 只收集业务必需信息 | 敏感信息脱敏处理 |
| **明确目的** | 告知信息用途 | 播报用途声明 |
| **安全保障** | 加密存储传输 | TLS加密+访问控制 |
| **期限限制** | 超过期限删除 | 90天后自动清理 |
| **可携权利** | 客户可导出数据 | 提供数据导出功能 |

### 敏感信息处理规则

```python
PIPL_SENSITIVE_FIELDS = {
    "身份证号": {
        "storage": "加密存储",
        "display": "脱敏显示：310***********1234",
        "access": "需二级权限"
    },
    "手机号": {
        "storage": "加密存储",
        "display": "脱敏显示：138****5678",
        "access": "客服可查看"
    },
    "银行卡号": {
        "storage": "仅存后四位",
        "display": "**** **** **** 1234",
        "access": "需风控授权"
    },
    "健康信息": {
        "storage": "高强度加密",
        "display": "不显示，仅用于核保",
        "access": "需医疗合规授权"
    }
}
```

### 录音/对话合规声明

```markdown
## 录音合规声明模板

---
【合规提醒】
为保障您的权益，本次通话将被录音。
录音将用于服务质量监控及争议处理，
保存期限为{保留期限}。

根据《个人信息保护法》，我们承诺：
• 仅在提供服务所必要的范围内使用您的信息
• 采取加密等技术措施保护您的信息安全
• 未经您的授权，不会向第三方提供您的个人信息

如您不同意录音，请在通话开始时告知坐席。
---
```
```

### 4. Renewal Reminder / 续期提醒

```python
RENEWAL_REMINDER_TEMPLATES = {
    "30天提醒": {
        "channel": "短信",
        "template": """
        【{保险公司}续期提醒】
        
        尊敬的{客户姓名}：
        
        您的保单（{保单号}）将于{到期日}到期，
        应缴保费{金额}元。
        
        为确保您的保障持续有效，
        请在{到期日前}完成续期缴费。
        
        💡温馨提示：
        • 逾期60天内仍可续期，但需重新计算等待期
        • 逾期60天后保单终止，保障失效
        
        续期方式：
        回复"1"：[链接]
        回复"2"：[方式2]
        回复"T"：[退订]
        """
    },
    
    "7天提醒": {
        "channel": "短信+电话",
        "template": """
        【重要提醒】
        
        {客户姓名}您好！
        
        ⚠️您的保单（{保单号}）
        仅剩7天即将到期！
        
        应缴保费：{金额}元
        截止日期：{到期日}
        
        如已缴费，请忽略此短信。
        如未缴费，请立即处理，避免保障中断。
        
        📞如有疑问，请拨打客服热线：{电话}
        """
    }
}
```

---

## Disclaimer

This skill provides insurance customer service tools for educational purposes. All services must comply with applicable insurance regulations and PIPL requirements.
