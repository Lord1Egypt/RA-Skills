---

name: mail-imap-sync
description: >
高性能 IMAP 邮件同步工具。支持多邮箱账号、增量同步、时间窗口过滤（recent/since/init 三模式），不影响邮箱邮件的阅读状态，只做本地拉取邮件分析和提炼功能。
自动将邮件解析为 Markdown 文件并按 年/月/日 树状结构存储。本工具具备去重、断点恢复、时区统一（Asia/ShangHai）
和高性能服务器过滤能力，适合构建邮件知识库、AI总结系统、通知系统等场景。
version: 3.0

inputs: []

outputs:

* name: synced_emails
  description: 本次同步成功保存的邮件文件路径列表

---

# 📬 Mail IMAP Sync Skill

## 🧠 功能概述

本技能用于：

* 📥 从 IMAP 邮箱同步邮件（支持 Gmail / 企业邮箱）
* ⚡ 高性能拉取（服务器端过滤，不扫全量）
* 🔁 自动增量（基于 UID）
* 🧱 本地结构化存储（Markdown + 时间分层）
* 🧠 为 AI 提供可读邮件数据源

---

## 🚀 支持的同步模式

### 🥇 1. init（纯增量模式）

```json
"mode": "init"
```

* 第一次运行：不拉历史邮件
* 后续：只同步新邮件

👉 适合长期运行系统

---

### 🥈 2. recent（推荐）

```json
"mode": "recent",
"recent_days": 7
```

* 第一次：拉取最近 N 天邮件
* 后续：自动增量

👉 推荐用于 AI 分析 / 日报

---

### 🥉 3. since（指定日期）

```json
"mode": "since",
"since": "2026-01-01"
```

* 第一次：拉取指定日期之后邮件
* 后续：增量同步

👉 用于历史导入

---

## 📁 存储结构

邮件以 Markdown 格式存储：

```
emails/
  {account}/
    YYYY/
      MM/
        DD/
          UID_MessageID_标题.md
```

---

## 🧾 邮件结构（标准化）

每封邮件包含：

```
# Subject

From: xxx
Date(raw): 原始时间
Date(local): 本地时间（Asia/ShangHai）
Date(ISO): ISO标准格式
Timestamp: Unix时间戳

UID: xxx
Message-ID: xxx
Account: xxx

---

正文内容
```

---

## ⏱ 时间处理（核心特性）

* 自动解析各种邮件时间格式
* 统一转换为：

  * Asia/ShangHai 时区
  * ISO标准格式
  * 时间戳（用于排序/分析）

👉 保证 AI 可稳定理解时间

---

## ⚡ 性能优化

本技能使用：

* IMAP SEARCH SINCE（服务器过滤）
* UID 增量同步
* 避免扫描整个邮箱

👉 支持万级邮件秒级同步

---

## 🔁 去重机制

* UID 去重
* Message-ID 去重
* 文件存在即跳过

---

## 🧱 稳定性保障

* state.json 原子写入（防损坏）
* Ctrl+C 不会丢状态
* 自动检测异常状态并修复
* 支持断点恢复

---

## ⚙️ 配置方式（config.json）

```json
{
  "accounts": [
    {
      "name": "bettermsao",
      "imap_host": "imap.gmail.com",
      "user": "xxx@gmail.com",
      "pass": "应用专用密码",
      "mode": "recent",
      "recent_days": 7
    }
  ]
}
```

---

## ▶️ 运行方式

```bash
./run.sh
```

---

## 📤 输出说明

返回：

```json
{
  "synced_emails": [
    "emails/.../xxx.md"
  ]
}
```

---

## 🧩 适用场景

* 📊 邮件数据分析
* 🤖 AI 邮件总结（日报 / 周报）
* 🚨 重要邮件监控
* 🧠 本地 LLM 数据输入

---

## 🔮 可扩展方向

* 邮件自动总结（LLM）
* 分类（订单 / 客户 / 系统）
* 向量化（语义搜索）
* 通知推送（微信 / Telegram）
* 多邮箱聚合分析

---

## ⚠️ 注意事项

* Gmail 需开启 IMAP 并使用应用专用密码
* 企业邮箱可能限制 IMAP 频率
* 初次运行建议使用 recent 模式

---

## 🏁 总结

本技能将邮件系统转化为：

👉 可结构化存储
👉 可被 AI 理解
👉 可持续增量更新