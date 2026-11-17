---
name: local-mail-digest
version: 2.0.0
description: 面向广大用户的本地邮件摘要与待办提取技能组件（零依赖、数据不出电脑）。把一批邮件变成结构化摘要（优先级/项目分组/待办/截止日），供 Python、Codex、Claude、WorkBuddy、Hermes、OpenClaw 等宿主调用。**主路径零配置**：宿主已接通邮箱连接器（如 WorkBuddy agent-mail/qq-mail）时，自动拉取邮件转 JSON 后本技能 `--input` 消费，用户无需任何授权码/IMAP 配置；自托管用户可选 IMAP 直连（配一次授权码）。输出 HTML/Markdown/JSON。
---
# 本地邮件摘要（local-mail-digest）

## 定位
本技能是**技能组件**，面向广大用户，不是个人定制、也不是独立产品。核心价值：把一堆邮件变成「待办 / 截止日 / 优先级」结构化清单，帮用户省时间。

**广大用户怎么用（零配置主路径）**：宿主（WorkBuddy / Codex / Claude / Hermes / OpenClaw）若已接通邮箱连接器（如 WorkBuddy 的 agent-mail、qq-mail），连接器负责拉邮件并转成 JSON，本技能只需 `--input` 消费这份 JSON。**用户连了邮箱即开箱即用，不用找授权码、不用开 IMAP。**

**自托管用户（可选）**：不连连接器、要数据完全自己掌控的，走 IMAP 直连（配一次授权码）。

核心卖点：**数据不出电脑**（邮件只在本机处理）、**零依赖**（仅 Python 标准库）、**零配置可达**（借宿主连接器）、**可私有化**。

## 功能
- **三入口**：①连接器消费（零配置，主推）②IMAP 直连（自托管，配一次授权码）③文本粘贴（兜底）
- 智能分层：高/中/低优先级（高优=含紧急/截止/需行动信号，语义判定，避免"未读被误判重要"）
- 项目分组、待办整句提取、截止日期识别
- 可选本地 LLM 增强（Ollama/Hermes 端点，真 AI 语义理解，失败自动降级关键词规则）
- 输出：HTML（人看）、Markdown、JSON（给 Agent 框架消费）
- 手机推送：SMTP 发自己、企业微信/飞书机器人

## 用法（推荐顺序）
```bash
# 1) 零配置主路径：宿主连接器已拉好邮件 → 转 JSON → 本技能消费（广大用户用它）
python digest.py --input 连接器导出的邮件.json --out 摘要.html --json 摘要.json

# 2) 自托管：IMAP 直连（配一次授权码，数据完全自己掌控）
python digest.py --imap me@qq.com --out 摘要.html --json 摘要.json

# 3) 兜底：文本粘贴（复制邮件正文存 txt）
python digest.py --txt 邮件.txt --out 摘要.html --json 摘要.json

# 可选：本地 LLM 增强（Ollama/Hermes 本地端点，不传则用规则）
python digest.py --input 连接器导出的邮件.json --llm http://localhost:11434/v1/chat/completions --model hermes3
```

## 零配置接入（host_adapter，广大用户主推）
宿主已连邮箱连接器（如 WorkBuddy agent-mail）时，用户**零授权码、零 IMAP 配置**即可用：
1. 宿主用连接器拉邮件，存成 `emails.json`（字段：`from, subject, date, body`）；
2. 调适配器生成摘要、可选推手机：
```bash
python host_adapter.py --emails-json emails.json --out 摘要.html --json 摘要.json
# 推手机（企微/飞书机器人）：
python host_adapter.py --emails-json emails.json --json 摘要.json --webhook https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx
```
适配器内部调用 `digest.py --input`，复用本技能的分类/抽取/推送能力。数据全程不出电脑。

## 被宿主集成（JSON 契约）
`--json` 输出结构：
```json
{
  "total": 3, "high": 2, "mid": 1, "low": 0,
  "emails": [
    {"from":"","subject":"","date":"","priority":"high|mid|low",
     "project":"","todos":[],"ddl":[],"summary":"","body_excerpt":""}
  ]
}
```
Agent 框架读取该 JSON 即可做后续动作（回复、建单、提醒）。

## 已知局限
- **IMAP 直连（自托管选项）真实连通需用户自测**：代码已兼容主流邮箱（SSL/STARTTLS 自动探测、UTF-7 中文文件夹解码、授权码提示），但本机无账号未实跑真实邮箱，部署前请用你的邮箱验证一次。零配置主路径（连接器消费）不走 IMAP，无此问题。
- **无本地 LLM 时为关键词规则**：复杂/模糊邮件可能漏抽或误判优先级；接入 Hermes（本地）/Ollama 端点即升级为真 AI 理解。
- 单封解析异常已被 try 隔离，不影响整体。
