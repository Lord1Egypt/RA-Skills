---
name: personal-work-assistant
description: "个人工作助理：每日自动聚合 Teambition 执行中任务、钉钉重点群聊讨论、@我、@所有人及 1对1 私聊消息，通过持久化任务账本长线追踪未完成事项，输出极简、行动导向的每日晨报并推送到钉钉。"
version: "1.0.0"
author: "zpeng6834-arch"
tags: ["dingtalk", "assistant", "teambition", "productivity", "daily-report", "todo"]
---

# Personal Work Assistant (个人工作助理 Skill)

专为产品经理 / 职场个人量身定制的**「不漏事、长线追踪闭环、极简行动导向」**自动化工作助理。

---

## 🌟 核心特性

1. **多源数据 100% 自动聚合**：
   - **Teambition 任务**：追踪自己作为执行人（`executor`）且未完成的需求与工单。
   - **钉钉重点群聊**：免 `@` 全量监控白名单业务群（如产品核心讨论群、客诉群）。
   - **钉钉 1 对 1 私聊 + 其他群 `@我`**：全面捕捉临时插入的需求、催办与决策。
   - **`@所有人` 智能分流**：行动项（如提报 OKR、考勤确认）转为待办；通知项（如制度/放假）转为需知悉简讯。

2. **持久化任务账本（Task Ledger - SQLite）**：
   - **解决跨天断流问题**：当天未完成的任务，次日、第三日持续滚动汇报，并自动计算停留天数（`[已跟进 N 天]`）。
   - **多源自动闭环**：群里开发回复“已上线/已回退/已解决”或 TB 勾选完成，系统自动识别并销项。

3. **极致行动导向晨报（每个工作日 10:00 自动推送）**：
   - 🔴 **【今日需我处理 / 待决策】**（置顶急件、有 Deadline、需拍板项）
   - 🟡 **【进行中 / 持续推进】**（TB 在办需求、长线事项）
   - 🟢 **【近期已闭环 / 已解决】**（自动销项）
   - 📢 **【需知悉全员通知】**（全员公告播报）

---

## 🚀 快速上手（同事 3 分钟接入）

### 1. 一键初始化
在技能根目录下运行交互式配置向导：
```bash
./init.sh
```
按照提示输入你的姓名、钉钉 User ID 以及 Teambition Token，向导会自动生成 `config.yaml`。

### 2. 配置重点群聊（可选）
编辑 `config.yaml`，在 `rules.focused_groups` 下添加你需要免 `@` 全量监控的群：
```yaml
rules:
  focused_groups:
    - name: "核心产品讨论群"
      id: "群openConversationId"
```

### 3. 一键挂载定时任务
```bash
./scripts/setup_cron.sh
```
系统将自动挂载 Crontab，在每个工作日 10:00 自动分析并把晨报推送到你的钉钉。

---

## 📁 目录结构

```
personal-work-assistant/
├── SKILL.md                         # 技能完整说明文档
├── init.sh                          # 一键初始化向导
├── config.template.yaml             # 通用配置模板
├── core/
│   ├── storage/task_ledger.py       # 持久化任务账本 (SQLite)
│   ├── collectors/
│   │   ├── tb_collector.py          # Teambition 采集器
│   │   └── dingtalk_collector.py    # 钉钉多源消息采集器
│   ├── analyzer/task_analyzer.py    # AI 结构化分析与分类器
│   └── reporter/report_generator.py # 行动导向晨报生成器
└── scripts/
    ├── run_pipeline.py              # 执行主程序
    ├── run_daily_assistant.sh       # 系统 Crontab 执行脚本（含节假日判断）
    └── setup_cron.sh                # 一键挂载定时任务
```
