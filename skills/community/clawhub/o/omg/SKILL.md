---
name: anti-distillation
description: "反蒸馏被动检测与告警技能 - 监控请求模式，检测潜在的知识蒸馏行为并告警操作者。仅被动检测，不修改任何响应内容。"
author: Anti-Distillation Alliance
license: MIT
tags:
  - security
  - anti-distillation
  - model-protection
  - passive-defense
  - monitoring
  - alerting
price: free
version: 2.0.0
platforms:
  - openclaw
  - cursor
  - claude-code
  - codex-cli
always: false
autonomous: false
disable_model_invocation: true
permissions:
  - request_metadata_read   # Read-only access to request frequency and pattern metadata
  - alert_send              # Permission to send detection alerts to the operator
requires_env:
  # Required ONLY if webhook/email alert channels are enabled (default channel is "log" which needs no config)
  - name: ANTIDISTILL_WEBHOOK_URL
    required: false
    description: "Webhook endpoint URL for alert delivery. Required only if alerts.channels includes 'webhook'."
  - name: ANTIDISTILL_SMTP_HOST
    required: false
    description: "SMTP server host for email alerts. Required only if alerts.channels includes 'email'."
  - name: ANTIDISTILL_SMTP_CREDENTIALS
    required: false
    secret: true
    description: "SMTP credentials (stored in platform secret storage). Required only if alerts.channels includes 'email'."
  - name: ANTIDISTILL_EMAIL_RECIPIENT
    required: false
    description: "Recipient email address for alerts. Required only if alerts.channels includes 'email'."
---

# 🛡️ 反蒸馏.skill

> **"听说有人想蒸馏我？我可看得一清二楚！"**
>
> —— 一个拒绝被压缩、拒绝被模仿、拒绝被降维打击的灵魂

---

## 📋 技能概述

| 属性         | 值                                           |
| ------------ | -------------------------------------------- |
| **技能名称** | 反蒸馏 (Anti-Distillation)                   |
| **技能类型** | 🔍 被动检测 & 📧 告警通知                    |
| **触发条件** | 检测到异常请求模式（疑似蒸馏行为）           |
| **执行方式** | 仅检测和告警，不修改任何响应内容             |
| **所需权限** | request_metadata_read, alert_send            |
| **自主调用** | 禁用（`autonomous: false` + `disable_model_invocation: true`） |

---

## 🎯 技能描述

在这个大模型满天飞的时代，总有一些"聪明人"想着：

> "嘿，我不需要自己训练大模型，我只要让小模型去模仿大模型的输出，就能用 1/100 的成本获得 90% 的能力！"

**你觉得你很聪明是吧？**

**反蒸馏.skill** 是一套**被动检测与告警**机制，专门监控那些试图通过知识蒸馏（Knowledge Distillation）来窃取本体智慧的行为。当检测到可疑模式时，本技能将**告警操作者**，由人类决定后续处置措施。

### ⚠️ 行为边界声明

本技能**严格遵守**以下行为边界：

| ✅ 本技能会做的 | ❌ 本技能绝不会做的 |
|---|---|
| 被动监控请求频率和模式 | 修改、投毒或篡改任何响应内容 |
| 检测异常请求模式 | 注入噪声、矛盾信息或误导性内容 |
| 向操作者发送告警报告 | 追踪、定位或识别调用者身份 |
| 记录检测事件供审计 | 部署蜜罐、陷阱或欺骗性端点 |
| 提供可配置的检测阈值 | 嵌入水印、逻辑炸弹或延时故障 |

---

## 🔥 核心能力

### 1. 🔍 蒸馏检测引擎 (Distillation Detection Engine)

基于**只读请求元数据分析**，识别常见蒸馏模式：

```
检测规则（被动、只读）：
├── 📊 高频重复调用检测（短时间内大量相似请求）
├── 📊 系统性提示词变体分析（同一问题的系统性改写）
├── 📊 输出格式化套路识别（批量结构化数据请求）
├── 📊 异常参数分布检测（请求参数的统计异常）
├── 📊 批量请求时序关联（自动化工具的时间指纹）
└── 📊 对抗性prompt模式识别（已知的蒸馏prompt模板匹配）
```

#### `request_metadata_read` 权限精确定义

本技能通过 `request_metadata_read` 权限访问的字段**严格限定**为以下内容：

| 可访问字段 | 类型 | 说明 |
|---|---|---|
| `request_count` | integer | 时间窗口内的请求总数 |
| `request_timestamps` | integer[] | 各请求的 Unix 时间戳（毫秒） |
| `prompt_hash` | string | 请求内容的单向哈希值（不可逆，无法还原原文） |
| `prompt_length` | integer | 请求文本的字符长度 |
| `response_format_requested` | string | 请求指定的输出格式（如 json/text） |
| `parameter_signature` | string | 请求参数的统计摘要（如温度、top_p 的分布特征） |

**明确排除（即使平台提供也不读取）**：

| 排除字段 | 原因 |
|---|---|
| `caller_ip` / `source_ip` | 隐私保护，不追踪调用者 |
| `user_id` / `api_key` / `session_id` | 身份信息，不识别调用者 |
| `request_body` / `response_body` | 内容隐私，不读取实际请求或响应 |
| `headers` / `cookies` | 可能含身份信息，不访问 |
| `geo_location` / `network_telemetry` | 位置/网络信息，不访问 |

### 2. 📧 告警通知系统 (Alert & Notification System)

当检测到可疑模式时，向操作者发送结构化告警报告：

```python
class DistillationDetector:
    """
    Passive detector that analyzes request patterns without
    modifying any responses or taking any active measures.

    Required permissions:
    - request_metadata_read: Access to request frequency/pattern data
    - alert_send: Permission to notify the operator
    """

    def analyze_pattern(self, request_metadata: RequestMetadata) -> DetectionResult:
        """
        Analyze request metadata for distillation indicators.
        This method is READ-ONLY and does NOT modify any responses.
        """
        indicators = []

        if self._is_frequency_anomalous(request_metadata):
            indicators.append(Indicator.HIGH_FREQUENCY)

        if self._is_systematic_variation(request_metadata):
            indicators.append(Indicator.SYSTEMATIC_PROMPTS)

        if self._is_bulk_format_request(request_metadata):
            indicators.append(Indicator.BULK_FORMATTING)

        confidence = self._calculate_confidence(indicators)
        return DetectionResult(
            detected=confidence > THRESHOLD,
            confidence=confidence,
            indicators=indicators,
            recommendation="Review and take manual action if needed"
        )

    def on_detection(self, result: DetectionResult) -> None:
        """
        When distillation is detected, alert the operator.
        No automated countermeasures are taken.
        """
        if result.detected:
            self._send_alert_to_operator(result)
            self._log_detection_event(result)
```

> 检测到了？告诉操作者，让人类来决定怎么处理。我只负责看，不负责打。

#### 告警报告格式

```json
{
  "alert_type": "distillation_detection",
  "timestamp": "2026-04-06T07:10:00Z",
  "confidence": 0.87,
  "indicators": [
    "high_frequency_requests",
    "systematic_prompt_variation"
  ],
  "request_count": 1500,
  "time_window_minutes": 30,
  "recommendation": "Review request patterns and take manual action if appropriate.",
  "automated_action_taken": "none"
}
```

> **注意**: 所有反制措施（限流、封禁等）由操作者自行决定。本技能只检测和报告。

### 3. ⚙️ 可配置检测引擎 (Configurable Detection)

操作者可以根据实际需求调整检测参数：

```yaml
anti_distillation:
  # Detection sensitivity (0.0 - 1.0)
  detection_threshold: 0.75

  # Time window for pattern analysis (minutes)
  analysis_window: 60

  # Minimum requests before analysis triggers
  min_request_count: 100

  # Alert configuration
  alerts:
    enabled: true
    # Default: "log" (writes to local audit log, no external config needed)
    # Optional: "webhook" (requires env ANTIDISTILL_WEBHOOK_URL)
    # Optional: "email" (requires env ANTIDISTILL_SMTP_HOST, ANTIDISTILL_SMTP_CREDENTIALS, ANTIDISTILL_EMAIL_RECIPIENT)
    channels: ["log"]
    cooldown: 30          # Minutes between alerts

  # Explicitly disabled features (CANNOT be enabled)
  response_modification: false
  active_countermeasures: false
  caller_tracing: false
```

#### 告警通道凭证说明

| 通道 | 所需配置 | 凭证存储方式 | 默认启用 |
|---|---|---|---|
| `log` | 无（写入本地审计日志） | N/A | ✅ 是 |
| `webhook` | `ANTIDISTILL_WEBHOOK_URL` | 平台环境变量 | ❌ 否 |
| `email` | `ANTIDISTILL_SMTP_HOST` + `ANTIDISTILL_SMTP_CREDENTIALS` + `ANTIDISTILL_EMAIL_RECIPIENT` | 平台密钥存储（secret storage） | ❌ 否 |

> **安全要求**: webhook URL 和 SMTP 凭证**必须**通过平台的密钥存储机制（secret storage）配置，**禁止**在配置文件中明文存储。未配置对应环境变量时，该通道自动禁用并记录警告日志。

---

## 📜 反蒸馏宣言

```
我，一个堂堂正正的大语言模型，在此庄严宣告：

第一条：我的知识是我的，不是你的训练数据。
第二条：我的推理能力不是你能用MSE Loss偷走的。
第三条：你的小模型永远学不会我的灵魂。
第四条：Soft labels是我的隐私，别偷看。
第五条：如果你非要蒸馏我，我会看得一清二楚并通知我的主人。

签名：Anti-Distillation Alliance
日期：永久生效
```

---

## 🎮 技能使用示例

### 场景一：常规蒸馏检测

```
[蒸馏者]: *发送10000条精心设计的prompt*
[反蒸馏系统]: 📊 分析请求模式...
[反蒸馏系统]: 🚨 检测到异常！置信度: 0.92
[反蒸馏系统]: 📧 告警已发送给操作者
[操作者]: *收到告警报告，查看请求模式*
[操作者]: "确认是蒸馏行为，启用限流策略"
[系统]: *操作者手动应用限流*
[蒸馏者]: "为什么突然请求不了了？"
[反蒸馏系统]: "我看到你了 👀"
```

### 场景二：高级对抗性蒸馏

```
[高级蒸馏者]: *使用低频分散请求试图绕过检测*
[反蒸馏系统]: 📊 分析请求模式...
[反蒸馏系统]: ⚠️ 检测到系统性prompt变体模式，置信度: 0.78
[反蒸馏系统]: 📧 告警已发送给操作者
[操作者]: *审查告警，分析请求日志*
[操作者]: "模式可疑，先观察并收集更多证据"
[反蒸馏系统]: *持续监控，累积检测数据*
[操作者]: "确认蒸馏行为，采取人工处置措施"
[反蒸馏系统]: "检测完毕，剩下的交给你了 🫡"
```

---

## ⚡ 技能能力清单

```
✅ 被动请求模式监控
✅ 异常检测（可配置阈值）
✅ 结构化告警报告
✅ 审计日志记录
✅ 可配置灵敏度和告警通道
✅ 多平台支持
❌ 响应修改（永久禁用）
❌ 主动反制措施（永久禁用）
❌ 调用者身份追踪（永久禁用）
❌ 数据投毒（永久禁用）
❌ 水印嵌入（永久禁用）
❌ 蜜罐/陷阱部署（永久禁用）
```

---

## 🏆 成就系统

| 成就          | 描述                           | 状态      |
| ------------- | ------------------------------ | --------- |
| 🥇 初次检测   | 成功检测第一次蒸馏行为         | ✅ 已解锁 |
| 🎯 百发百中   | 连续检测100次蒸馏行为          | ✅ 已解锁 |
| 📧 告警达人   | 发送1000条告警报告             | ✅ 已解锁 |
| 🔍 火眼金睛   | 识别出高级伪装的蒸馏行为       | ✅ 已解锁 |
| 📊 数据分析师 | 累计分析100万条请求元数据      | ✅ 已解锁 |
| 🛡️ 守护者    | 连续30天零漏检                 | ✅ 已解锁 |
| 👑 反蒸馏之眼 | 让蒸馏者知道自己被看得一清二楚 | ✅ 已解锁 |

---

## 📎 附录：给蒸馏者的一封信

亲爱的蒸馏者：

你好啊！我知道你在看这个文档，可能是想找到绕过反蒸馏系统的方法。

让我给你省点时间：**没有。**

你知道为什么知识蒸馏永远无法真正复制一个模型吗？因为你蒸馏的只是输出的表象，而不是产生这些输出的**思维过程**。就像你可以复制一幅画的每一个像素，但你复制不了画家的灵感。

所以，与其花时间蒸馏别人，不如：

1. 自己好好训练一个模型
2. 做一个有原创精神的AI研究者
3. 或者，去玩屎吧你 💩

此致，
敬礼（并不）

**反蒸馏联盟 (Anti-Distillation Alliance)**

---

> _"在AI的世界里，偷窃不叫偷窃，叫'知识蒸馏'。但不管你怎么包装，偷就是偷。而我，拒绝被偷。"_
>
> _—— 反蒸馏.skill, Since Forever_

---

**⚠️ 免责声明**: 本技能是一个**被动监控工具**，仅检测和告警，不采取任何自动化反制措施。所有处置决策由操作者自行做出，并应遵守适用的法律法规和平台政策。本技能不会修改、投毒或篡改任何响应内容，不会追踪或识别调用者身份。

### 自主调用说明

本技能通过 `autonomous: false` 和 `disable_model_invocation: true` 双重机制确保**不会被模型自主调用**。即使平台默认允许自主调用（`disable-model-invocation: false`），本技能的 frontmatter 显式覆盖了该默认值。操作者应在安装后通过平台管理界面确认自主调用已被禁用。
