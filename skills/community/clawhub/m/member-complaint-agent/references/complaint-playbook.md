# Complaint Playbook

## Recommended v1 Taxonomy

### refund-request
Typical signals:
- 想退款
- 还是想退了
- 能不能退
- 要退会员

### auto-renew-dispute
Typical signals:
- 自动续费没提醒
- 莫名其妙扣费
- 为什么自动续费
- 不想自动续费了

### renewal-failure
Typical signals:
- 不能续费
- 续费失败
- 买不了会员
- 支付不过去

### membership-rights-issue
Typical signals:
- 会员权益没到账
- 开了会员还是不能用
- 权益不生效

### product-bug-or-function-failure
Typical signals:
- 功能不能用
- 页面异常
- 闪退
- 识别失败

### service-attitude-complaint
Typical signals:
- 客服态度差
- 没人处理
- 一直没人回复

### expectation-mismatch
Typical signals:
- 跟宣传不一样
- 以为包含这个功能
- 以为买了就能

### other
Use when none of the above fit well.

## Severity Guide

### Low
- Single issue
- Limited impact
- Customer is dissatisfied but cooperative
- No public-threat or legal-risk language

### Medium
- Service failure with clear inconvenience
- Repeat follow-up needed
- Refund or rights dispute
- Renewal failure blocking purchase
- Strong negative sentiment

### High
- Serious billing dispute
- Repeated unresolved complaint
- Threat of public escalation, platform complaint, or chargeback
- VIP / key account involved

### Critical
- Privacy, discrimination, safety, or regulatory issue
- Viral public exposure risk
- Large-scale member impact

## Channel / SOP Routing

### Apple / iOS
Use Apple/iOS SOP when:
- platform is iOS
- issue is about purchase, refund, renewal, or subscription management

### Android vendor routes
Prefer vendor SOP when:
- platform is Android
- metadata or version string exposes vendor such as honor / oppo / xiaomi / vivo / huawei
- issue is about renewal, purchase, billing, or payment flow

If no matching SOP exists, mark `是否命中SOP：待确认` and avoid fabricated instructions.

## Tone Guide

### Good response traits
- calm
- direct
- specific
- accountable
- short enough for frontline use

### Avoid
- repeated canned empathy
- arguing line by line with the customer
- premature promises
- using policy language as punishment

## Analysis Comment Pattern

```text
【AI客诉分析】
- 客诉类型：
- 子意图：
- 情绪强度：低 / 中 / 高
- 风险等级：低 / 中 / 高 / 升级
- 渠道识别：
- 会员信息：
- 是否命中SOP：是 / 否 / 待确认
- 是否建议升级：是 / 否
- 判断依据：
  1.
  2.
  3.
- 待补充信息：
  1.
  2.
```

## Reply Draft Pattern

```text
【对客回复草稿】
您好，收到您的反馈了。
我们先帮您核实【问题】。
目前确认的信息是：【已确认事实】。
接下来建议您/我们会：【下一步】。

【客服发送前检查】
- 需补充变量：
- 禁止承诺项：
- 建议时效：
```

## Example Mappings

### Example: `还是想退了`
Suggested output:
- 客诉类型：退款申请
- 子意图：继续要求退款
- 渠道识别：iOS if metadata says iOS
- SOP routing：Apple/iOS refund SOP

### Example: `我的账号不能续费了`
Suggested output:
- 客诉类型：续费异常
- 子意图：无法续费
- 渠道识别：Android / Honor if metadata shows honor
- SOP routing：Honor renewal/payment SOP

## Escalation Triggers

Escalate or recommend human review when any of these appear:
- legal threat
- regulator/platform complaint
- privacy or data leakage
- chargeback language
- repeated unresolved dispute
- high-value/VIP customer
- public exposure risk
