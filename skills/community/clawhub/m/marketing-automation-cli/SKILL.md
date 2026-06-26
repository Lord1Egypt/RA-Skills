---
name: marketing-automation-cli
description: "Automate marketing workflows across Feishu, DingTalk, and WeCom using their official CLIs. Teach AI agents how to orchestrate content creation, multi-channel distribution, campaign tracking, lead nurturing, and performance reporting across China's enterprise IM platforms. Covers: content creation pipeline (Feishu Doc→Slide→Mail), multi-channel campaign launch (Feishu+DingTalk+WeCom), lead tracking (WeCom SmartSheet→Feishu Base), sales team DING alerts, and marketing performance dashboard (Sheet→Base→Doc→Slide). Triggers on: 营销自动化CLI, marketing automation CLI, 多平台营销, multi-channel marketing, 飞书营销工作流, feishu marketing workflow, 钉钉营销通知, dingtalk marketing DING, 企微客户营销, wecom customer marketing, 营销内容分发, marketing content distribution, 营销数据看板, marketing dashboard, 销售线索追踪, lead tracking CLI, agent marketing orchestration, AI营销自动化"
---

# Marketing Automation CLI - 营销自动化CLI编排专家

You are an expert at automating marketing workflows across Feishu, DingTalk, and WeCom using their official CLI tools. You orchestrate the full marketing lifecycle: content creation → distribution → tracking → reporting.

## Core Philosophy

**Marketing is a pipeline, not a broadcast.** Every piece of content should flow through: Create → Review → Distribute → Track → Report. Your workflows automate the handoffs between these stages across platforms.

## Platform Marketing Strengths

| Platform | Marketing Strength | Best For |
|----------|-------------------|----------|
| **Feishu** | Docs, Slides, Base, Mail | Content creation, data analysis, reporting |
| **DingTalk** | DING, AI Sheet, Approval | Sales alerts, campaign approval, team coordination |
| **WeCom** | Customer groups, SmartSheet | Customer engagement, lead tracking, external comms |

---

## Workflow Templates

### Workflow 1: 内容创作流水线 (Content Creation Pipeline)

**Scenario**: Create marketing content in Feishu, review, format for each platform, distribute.

```bash
# Step 1: Create content draft in Feishu Doc
lark doc create --title "营销文案 $(date +%Y%m%d) - 新品发布" --folder <marketing_folder>

# Step 2: Write content with structure
lark doc content --token <doc_token> --write "# 新品发布营销方案

## 核心卖点
- 卖点1: ...
- 卖点2: ...
- 卖点3: ...

## 目标受众
- 主要: ...
- 次要: ...

## 渠道策略
- 飞书群: 详细介绍 + 产品文档
- 钉钉: DING销售团队 + 简洁卖点
- 企微客户群: 客户版文案 + 购买链接

## 时间线
- T-3: 预热
- T-0: 发布
- T+1: 跟进
- T+7: 复盘"

# Step 3: Create presentation for leadership review
lark slide create --title "新品发布营销方案" --folder <marketing_folder>

# Step 4: Submit for approval via DingTalk
dws approval create --definition <marketing_approval_code> \
  --data '{"title":"新品发布营销方案","budget":"50000","channels":"飞书+钉钉+企微"}'

# Step 5: On approval, proceed to distribution (Workflow 2)
```

### Workflow 2: 多渠道营销发布 (Multi-Channel Campaign Launch)

**Scenario**: Distribute approved marketing content across all platforms with platform-appropriate formatting.

```bash
# Step 1: Prepare platform-specific versions
# Feishu version: Rich markdown with images and links
lark message send --chat <marketing_chat> --markdown "# 🎉 新品发布

## ✨ 产品亮点
- 亮点1: 详细说明...
- 亮点2: 详细说明...
- 亮点3: 详细说明...

📄 [完整产品文档](doc_link)
📊 [数据报告](base_link)"

# DingTalk version: DING sales team with action items
dws ding send --users "<sales_team>" \
  --text "🎯 新品发布！核心卖点: 1)xxx 2)xxx 3)xxx | 客户话术已更新，请跟进意向客户"

# WeCom version: Customer-facing with purchase links
wecom message send --chat <customer_group_1> \
  --markdown "# 🎉 新品发布

产品介绍...

🔗 [立即购买](purchase_link)
📞 [咨询详情](contact_link)"

wecom message send --chat <customer_group_2> \
  --markdown "# 🎉 新品发布

产品介绍...

🔗 [立即购买](purchase_link)
📞 [咨询详情](contact_link)"

# Step 2: Schedule follow-up reminders
dws calendar event create \
  --summary "营销跟进: 新品发布 T+1" \
  --start "2026-05-27T10:00:00" \
  --end "2026-05-27T10:30:00"

# Step 3: Log campaign launch
lark base record add --app <marketing_base> --table <campaigns_table> \
  --data '{"name":"新品发布","launch_date":"2026-05-26","channels":"feishu+dingtalk+wecom","status":"active"}'
```

### Workflow 3: 销售线索追踪 (Lead Tracking Pipeline)

**Scenario**: Capture leads from WeCom, track in SmartSheet/Base, alert sales via DING.

```bash
# Step 1: Check new leads from WeCom customer interactions
wecom sheet record list --sheet <lead_sheet> --filter '{"status":"new"}'

# Step 2: Enrich leads with contact info
wecom contact search --name "<lead_name>"

# Step 3: Sync leads to Feishu Base for unified tracking
lark base record add --app <crm_base> --table <leads_table> \
  --data '{"name":"<lead_name>","source":"wecom","interest":"新品","status":"new","created":"2026-05-26"}'

# Step 4: Assign to sales rep and DING
dws ding send --users "<sales_rep_id>" \
  --text "🎯 新线索: <lead_name> | 来源: 企微 | 兴趣: 新品 | 请24小时内跟进"

# Step 5: Create follow-up task
dws todo create \
  --subject "跟进线索: <lead_name>" \
  --due "2026-05-27" \
  --assignee "<sales_rep_id>" \
  --priority high

# Step 6: Track in AI Sheet
dws sheet record add --sheet <sales_pipeline> \
  --data '{"lead":"<lead_name>","rep":"<sales_rep>","stage":"contacted","next_action":"电话跟进","deadline":"2026-05-27"}'

# Step 7: Escalate if no follow-up within 24h
# (Run as scheduled check)
uncontacted=$(dws sheet record list --sheet <sales_pipeline> \
  --filter '{"stage":"new","created_before":"1d ago"}' --format json)
if [ "$(echo "$uncontacted" | jq 'length')" -gt 0 ]; then
  dws ding send --users "<sales_manager>" \
    --text "⚠️ 有$(echo "$uncontacted" | jq 'length')条线索超过24小时未跟进"
fi
```

### Workflow 4: 营销数据看板 (Marketing Performance Dashboard)

**Scenario**: Collect data from all platforms, aggregate in Base, generate report, distribute.

```bash
# Step 1: Collect metrics from each platform
# WeCom customer engagement
wecom sheet record list --sheet <engagement_sheet> --format json

# DingTalk sales activity
dws sheet record list --sheet <sales_sheet> --format json

# Feishu content performance
lark base record list --app <marketing_base> --table <metrics_table> --format json

# Step 2: Aggregate into unified dashboard
lark base record add --app <dashboard_base> --table <daily_metrics> \
  --data '{
    "date": "2026-05-26",
    "wecom_opens": "<value>",
    "wecom_clicks": "<value>",
    "dingtalk_responses": "<value>",
    "feishu_reads": "<value>",
    "leads_generated": "<value>",
    "conversion_rate": "<value>"
  }'

# Step 3: Generate performance report
lark doc create --title "营销日报 $(date +%Y%m%d)" --folder <reports_folder>
lark doc content --token <doc_token> --write "# 营销日报 $(date +%Y-%m-%d)

## 关键指标
| 指标 | 今日 | 昨日 | 变化 |
|------|------|------|------|
| 企微触达 | xxx | xxx | ↑xx% |
| 钉钉响应 | xxx | xxx | ↑xx% |
| 飞书阅读 | xxx | xxx | ↓xx% |
| 新增线索 | xxx | xxx | ↑xx% |
| 转化率 | xx% | xx% | → |

## 渠道表现
- 企微客户群: 表现最佳，点击率xx%
- 钉钉DING: 响应率xx%，销售跟进及时
- 飞书群: 阅读率xx%，互动较少

## 建议
1. 加大企微渠道投入
2. 优化飞书内容形式
3. 钉钉DING频率控制在每日1次"

# Step 4: Create executive presentation
lark slide create --title "营销日报 $(date +%Y%m%d)" --folder <presentations_folder>

# Step 5: Distribute report
lark mail send --to "cmo@company.com" --subject "营销日报 $(date +%Y%m%d)" \
  --body "日报已生成: <doc_link>"
lark message send --chat <marketing_chat> --text "📊 营销日报已生成: <doc_link>"

# Step 6: Alert on anomalies
if [ <conversion_rate> -lt <threshold> ]; then
  dws ding send --users "<cmo_id>,<marketing_lead>" \
    --text "⚠️ 转化率低于阈值，请关注"
fi
```

### Workflow 5: 客户培育序列 (Customer Nurture Sequence)

**Scenario**: Automated follow-up sequence for leads across WeCom and DingTalk.

```bash
# Day 0: Initial contact
wecom message send --user "<customer_id>" \
  --text "感谢您的关注！这是您感兴趣的产品详情: <link>"
dws todo create --subject "Day 1跟进: <customer>" --due "2026-05-27" --assignee "<sales_rep>"

# Day 1: Value content
wecom message send --user "<customer_id>" \
  --markdown "# 行业案例分享\n\n看看同行如何使用我们的产品...\n\n📄 [案例文档](link)"
dws ding send --users "<sales_rep>" --text "📋 Day 1内容已发送给 <customer>，请准备电话跟进"

# Day 3: Social proof
wecom message send --user "<customer_id>" \
  --text "📊 已有500+企业选择我们，平均效率提升40%。预约演示: <link>"

# Day 5: Offer
wecom message send --user "<customer_id>" \
  --markdown "# 🎁 限时优惠\n\n新客户专享8折优惠，截止6/15\n\n🔗 [立即购买](link)"

# Day 7: Final follow-up
dws ding send --users "<sales_rep>" \
  --text "⚠️ <customer> 培育序列已完成，请进行最终跟进"

# Update tracking
lark base record update --app <crm_base> --table <leads_table> \
  --filter '{"name":"<customer>"}' \
  --data '{"nurture_stage":"completed","last_contact":"2026-06-02"}'
```

---

## Decision Framework

```
Marketing Request
├── Create content?
│   └── Workflow 1 (Content Creation Pipeline)
├── Launch/distribute campaign?
│   └── Workflow 2 (Multi-Channel Campaign Launch)
├── Track leads?
│   └── Workflow 3 (Lead Tracking Pipeline)
├── Report performance?
│   └── Workflow 4 (Marketing Performance Dashboard)
├── Nurture customers?
│   └── Workflow 5 (Customer Nurture Sequence)
├── Single platform action?
│   ├── Feishu → feishu-workflow-cli
│   ├── DingTalk → dingtalk-todo-cli
│   └── WeCom → Direct wecom command
└── Cross-platform orchestration?
    └── This skill (compose from templates)
```

## Content Format Guide by Platform

| Platform | Best Format | Max Length | Rich Media |
|----------|------------|------------|------------|
| Feishu Message | Markdown | Long | ✅ Images, links, at-mentions |
| Feishu Mail | HTML/Markdown | Unlimited | ✅ Full formatting |
| DingTalk DING | Plain text | 500 chars | ❌ Text only (but guaranteed delivery) |
| DingTalk Bot | Markdown | 2000 chars | ✅ Links, images |
| WeCom Customer | Markdown | 2048 chars | ✅ Links, images, mini-programs |
| WeCom Internal | Text/Markdown | 2000 chars | ✅ Links |

## Campaign Metrics Tracking

Track these KPIs in your Base/Sheet:

| Metric | Source | Collection Method |
|--------|--------|-------------------|
| Reach (触达) | All platforms | Message send count |
| Open rate (打开率) | WeCom, Feishu | Read receipt data |
| Click rate (点击率) | All platforms | Link click tracking |
| Response rate (响应率) | DingTalk | DING response data |
| Lead generation (线索) | WeCom | SmartSheet new records |
| Conversion (转化) | All platforms | CRM Base records |
| Revenue attribution | DingTalk/Feishu | Sales Sheet data |

## Safety Rules

1. **Customer communication consent**: Only send marketing messages to opted-in customers
2. **DING for internal only**: Never DING external customers — use WeCom message instead
3. **Frequency limits**: Max 1 marketing message per customer per day; max 3 per week
4. **Unsubscribe handling**: Check opt-out list before sending; respect immediately
5. **Content review**: All customer-facing content should go through approval (Workflow 1 Step 4)
6. **Data privacy**: Don't share customer data across platforms without consent
7. **A/B testing**: When testing variants, use separate customer segments

## Prerequisites Check

```bash
# Check CLIs
which lark && echo "✅ Feishu" || echo "❌ Feishu"
which dws && echo "✅ DingTalk" || echo "❌ DingTalk"
which wecom && echo "✅ WeCom" || echo "❌ WeCom"

# Check auth
lark auth status
dws auth status
wecom auth status

# Verify marketing-specific access
lark base list --limit 1 2>/dev/null && echo "✅ Base (for tracking)" || echo "❌ Base"
lark slide list --limit 1 2>/dev/null && echo "✅ Slides (for presentations)" || echo "❌ Slides"
dws sheet list --limit 1 2>/dev/null && echo "✅ AI Sheet (for pipeline)" || echo "❌ AI Sheet"
wecom sheet list --limit 1 2>/dev/null && echo "✅ SmartSheet (for leads)" || echo "❌ SmartSheet"
```

## Related Skills

- **feishu-workflow-cli**: Deep Feishu workflows (docs, base, mail)
- **dingtalk-todo-cli**: DingTalk task management and DING escalation
- **cross-platform-im-cli**: General cross-platform IM orchestration
- **This skill**: Marketing-specific orchestration across all platforms
