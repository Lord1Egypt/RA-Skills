---
name: opik-reporter
version: 1.0.0
description: Opik observability reporter - fetches traces, analyzes usage, costs, and errors, then sends reports to Discord.
author: sunnyhot
license: MIT
keywords:
  - opik
  - observability
  - tracing
  - cost-analysis
  - discord
---

# Opik Reporter - Opik 可观测性报告器

**自动获取 Opik 追踪数据，分析使用量和成本，发送报告到 Discord**

---

## ✨ 核心功能

### 🔍 **追踪分析**
- ✅ 获取最近的 traces 和 spans
- ✅ 分析 LLM 调用
- ✅ 分析工具调用
- ✅ 识别错误和失败

### 📊 **使用量统计**
- ✅ Token 使用量
- ✅ 成本统计
- ✅ 请求数量
- ✅ 成功率

### 📈 **报告生成**
- ✅ 每小时摘要报告
- ✅ 每日详细报告
- ✅ 错误报告
- ✅ 成本优化建议

### 💬 **Discord 推送**
- ✅ 自动推送到 Discord 子区
- ✅ 格式化的报告
- ✅ 错误告警

---

## 🚀 **使用方法**

### **1. 自动报告模式**（推荐）

创建定时任务，每小时发送一次报告：

```bash
openclaw cron add \
  --name "opik-reporter" \
  --cron "0 * * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --wake now \
  --deliver \
  --message "运行 opik-reporter: 获取 Opik 追踪数据，生成报告。报告格式用中文。"
```

---

### **2. 手动触发分析**

```bash
node /Users/xufan65/.openclaw/workspace/skills/opik-reporter/scripts/reporter.cjs
```

**功能**:
- 获取最近的追踪数据
- 分析使用量和成本
- 生成报告
- 推送到 Discord

---

## 📋 **报告格式**

### **每小时报告**

```
📊 Opik 追踪报告

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

时间范围: 最近 1 小时

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 使用量统计

总请求数: 15
成功率: 93.3%

Token 使用:
  输入: 12,345
  输出: 6,789
  总计: 19,134

成本:
  总计: $0.05

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 工具调用

总调用: 45 次
最常用:
  • web_search (15次)
  • read (12次)
  • exec (10次)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ 错误 (1个)

• timeout in deals-morning (2分钟前)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 优化建议

1. deals-morning 超时，建议增加超时时间
```

---

## 🔧 **配置文件**

### `config/settings.json`

```json
{
  "opik": {
    "apiKey": "I5xMCUAO14m4EyckFWfqQla3O",
    "workspace": "default",
    "project": "openclaw"
  },
  "discord": {
    "channel": "discord",
    "to": "channel:1481801666851373138"
  },
  "reportSchedule": {
    "hourly": true,
    "daily": true,
    "onError": true
  }
}
```

---

## 📝 **更新日志**

### v1.0.0 (2026-03-13)
- ✅ 初始版本
- ✅ 追踪分析
- ✅ 使用量统计
- ✅ 报告生成
- ✅ Discord 推送

---

**🚀 让你的 Opik 追踪数据更加可视化和可操作！**
