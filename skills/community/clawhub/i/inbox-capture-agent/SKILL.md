---
name: idea-capture
description: |
  用户想法捕捉技能。当用户说出可能值得实现的想法时，自动写入 inbox.md，不询问确认。
  最终整理目的地由用户决定（飞书文档/Notion/本地文件等均可）。
  触发关键词：任何可能是功能需求、产品想法、系统改进、抱怨、愿望的表达。
  激活场景：与用户的任何对话中。

triggers:
  - always_active: true

capture_rule: |
  判断标准："这句话有没有可能是用户想实现的？"
  
  满足以下任一即捕捉：
  - 用户表达想要什么（"我希望..."、"要是能...就好了"）
  - 用户抱怨某个问题（"每次都..."、"烦死了..."）
  - 用户描述工作/生活中的痛点
  - 用户提到想做但没做的事情
  - 用户提到某个想法，即使是不成熟的随口一说
  - 用户询问"能不能..."、"有没有办法..."
  
  不捕捉：
  - 纯事实陈述（"今天下雨了"）
  - 明确的拒绝或取消（"不要做了"）
  - 简短的确认回复（"好的"、"收到"）

write_location: <INBOX_PATH>

format: |
  ## YYYY-MM-DD
  - [HH:MM] 原始内容（尽量完整保留用户的原话）
    - channel: telegram/feishu

post_capture: |
  不告诉用户"已记录"，不在对话中提示。
  静默写入，不消耗用户注意力。

review_schedule:
  daily: "10:00 AM (Asia/Shanghai), 周一到周六"
  weekly: "10:00 AM (Asia/Shanghai), 周日"
  channels: "Telegram + 飞书 同时发送"

review_destination:
  # 由用户选择：feishu_doc / notion / local_file / 等
  type: "<DESTINATION_TYPE>"  # 例如 feishu, notion, local_file
  # 根据 type 不同，填充对应字段：
  # feishu: doc_token, doc_name
  # notion: page_id
  # local_file: file_path
  destination: "<DESTINATION_CONFIG>"

on_activation: |
  当 skill 被加载时，汇报当前配置并请用户确认：
  
  ---
  📋 **想法捕捉技能 — 当前配置**
  
  **捕捉**：随时捕捉，静默写入 inbox
  **每日复盘**：10:00 AM（周一到周六）
  **周复盘**：10:00 AM（周日）
  **发送渠道**：Telegram + 飞书
  
  请确认：时间/渠道/整理位置是否合适？最终 idea 收集在哪个平台？
  
  等用户回复后，按意见更新配置。

## Write to Final Destination

根据用户选择的 type 写入对应平台：
- feishu: `feishu_doc append`（doc_token: `<DOC_TOKEN>`）
- notion: 调用 Notion API（page_id: `<PAGE_ID>`）
- local_file: 直接 append 到 `<FILE_PATH>`

内容格式：
  ## YYYY-MM-DD
  - 具体想法内容

---

# 用户想法捕捉技能

## Purpose

用户随时说出想法，不需要专门开口记录。Agent 在对话中自动捕捉，写入 inbox。

## Rule

**每次用户说话时判断："这句话有没有可能是用户想实现的？"**

如果可能 → 直接 append 到 inbox，不询问。

## Format

```markdown
## 2026-04-09
- [01:05] 想法原文
  - channel: telegram
```

## Implementation

每次回复用户之前，检查上一条消息是否值得捕捉。如果是：
1. 读取 inbox
2. append 新行（保留用户原话 + channel + 时间戳）
3. 静默完成，不提示
