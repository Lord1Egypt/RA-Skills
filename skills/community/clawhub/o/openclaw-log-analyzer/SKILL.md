---
name: log-analyzer
version: 1.0.0
description: Intelligent log analysis tool for monitoring cron jobs, detecting errors, analyzing patterns, and generating reports. Supports automatic error detection, log aggregation, and Discord notifications.
author: sunnyhot
license: MIT
keywords:
  - log-analyzer
  - error-detection
  - cron-monitoring
  - log-aggregation
  - discord-notifications
---

# Log Analyzer - 智能日志分析工具

**监控你的系统日志，自动检测错误，生成分析报告**

---

## ✨ 核心功能

### 🎯 **日志监控**
- ✅ 监控 OpenClaw cron jobs 日志
- ✅ 监控系统日志文件
- ✅ 实时日志流分析
- ✅ 多日志源聚合

### 🔍 **错误检测**
- ✅ 自动检测错误模式
- ✅ 识别异常日志
- ✅ 错误分类（ERROR/WARN/INFO）
- ✅ 错误频率统计

### 📊 **模式分析**
- ✅ 识别常见错误模式
- ✅ 检测重复错误
- ✅ 错误趋势分析
- ✅ 时间序列分析

### 📈 **报告生成**
- ✅ 每日/每周/每月报告
- ✅ 错误摘要
- ✅ 性能指标
- ✅ 推送到 Discord

---

## 📂 **日志源**

### **1. OpenClaw Cron Jobs** ⭐⭐⭐⭐⭐
**位置**: `/Users/xufan65/.openclaw/logs/`

**监控内容**:
- ✅ 定时任务执行日志
- ✅ 错误堆栈信息
- ✅ 性能指标
- ✅ 任务状态

**示例日志**:
```
2026-03-12 08:00:00 [ERROR] deals-morning - Timeout after 120s
2026-03-12 09:00:00 [INFO] content-research - Completed in 88s
2026-03-12 10:00:00 [WARN] tech-news-digest - Slow response 150s
```

---

### **2. 系统日志**
**位置**: `/var/log/`

**监控内容**:
- ✅ 系统错误
- ✅ 网络错误
- ✅ 磁盘空间
- ✅ 内存使用

---

### **3. 应用日志**
**位置**: 自定义路径

**监控内容**:
- ✅ 应用错误
- ✅ API 调用
- ✅ 用户行为
- ✅ 性能数据

---

## 🔍 **错误检测规则**

### **高优先级错误**（立即通知）
- ❌ 任务执行失败
- ❌ 超时错误
- ❌ API 调用失败
- ❌ 内存溢出
- ❌ 磁盘空间不足

### **中优先级错误**（每日报告）
- ⚠️ 性能下降
- ⚠️ 响应时间过长
- ⚠️ 重试次数过多
- ⚠️ 依赖版本过旧

### **低优先级错误**（每周报告）
- ℹ️ 信息日志
- ℹ️ 调试日志
- ℹ️ 成功操作

---

## 📊 **报告类型**

### **1. 实时报告**（错误发生时）
```
❌ 检测到错误！

任务: deals-morning
时间: 2026-03-12 09:00:00
错误: Timeout after 120s
影响: 羊毛推荐推送失败

建议:
1. 增加超时时间到 300s
2. 检查网络连接
3. 联系 API 提供商
```

---

### **2. 每日报告**（每晚 22:00）
```
📊 每日日志分析报告

日期: 2026-03-12
任务数: 14
成功: 12
失败: 2

❌ 失败任务:
- deals-morning (09:00)
- tech-news-digest (09:10)

⚠️ 性能警告:
- content-research 响应时间 150s
- video-ideas-daily 超时 1 次

📈 性能指标:
- 平均执行时间: 95s
- 最大执行时间: 600s (deals-evening)
- 最小执行时间: 5s (daily-update)

💡 建议:
1. deals-morning 超时，建议增加到 300s
2. content-research 性能下降，建议优化
```

---

### **3. 每周报告**（周日 22:00）
```
📊 每周日志分析报告

周期: 2026-03-06 ~ 2026-03-12
总任务执行: 98 次
成功率: 94.9%

📈 趋势分析:
- 错误率: ↓ 下降 5%
- 性能: ↑ 提升 10%
- 超时次数: ↓ 减少 3 次

🏆 表现最佳:
1. skill-sync (100% 成功率)
2. failure-monitor (100% 成功率)
3. daily-update (100% 成功率)

⚠️ 需要关注:
1. deals-morning (85% 成功率)
2. tech-news-digest (87% 成功率)

💡 优化建议:
1. 调整超时时间
2. 优化网络请求
3. 增加重试机制
```

---

## 🚀 **使用方法**

### **1. 自动监控模式**（推荐）

创建定时任务，每 30 分钟检查一次：

```bash
openclaw cron add \
  --name "log-analyzer" \
  --cron "*/30 * * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --wake now \
  --deliver \
  --message "运行 log-analyzer: 分析系统日志，检测错误，生成报告。报告格式用中文。"
```

---

### **2. 手动触发分析**

```bash
node /Users/xufan65/.openclaw/workspace/skills/log-analyzer/scripts/analyzer.cjs
```

**功能**:
- 扫描所有日志文件
- 分析错误模式
- 生成报告
- 推送到 Discord

---

### **3. 查看当前状态**

```bash
cat /Users/xufan65/.openclaw/workspace/memory/log-analyzer-status.json
```

**包含内容**:
- 最后分析时间
- 检测到的错误
- 错误趋势
- 优化建议

---

## 📋 **工作流程**

```
定时扫描 (每30分钟)
   ↓
扫描日志文件
   ↓
分析日志内容
   ↓
   ├─ 检测到错误 → 立即通知
   └─ 正常 → 记录状态
   ↓
生成报告
   ↓
推送到 Discord
   ↓
更新状态文件
```

---

## 🔧 **配置文件**

### `config/rules.json`

```json
{
  "errorPatterns": [
    {
      "pattern": "ERROR|error|Error",
      "priority": "high",
      "category": "error"
    },
    {
      "pattern": "WARN|warn|Warning",
      "priority": "medium",
      "category": "warning"
    },
    {
      "pattern": "timeout|Timeout|TIMEOUT",
      "priority": "high",
      "category": "timeout"
    }
  ],
  "logSources": [
    {
      "name": "openclaw-cron",
      "path": "/Users/xufan65/.openclaw/logs/*.log",
      "enabled": true
    },
    {
      "name": "system",
      "path": "/var/log/system.log",
      "enabled": false
    }
  ],
  "reportSchedule": {
    "daily": "22:00",
    "weekly": "sunday 22:00",
    "monthly": "last-day 22:00"
  },
  "notifications": {
    "onError": true,
    "onWarning": false,
    "channel": "discord",
    "to": "channel:1478698808631361647"
  }
}
```

---

## 📊 **状态文件**

### `memory/log-analyzer-status.json`

```json
{
  "lastScan": "2026-03-12T17:30:00+08:00",
  "errors": {
    "today": 2,
    "week": 5,
    "month": 15
  },
  "warnings": {
    "today": 5,
    "week": 12,
    "month": 30
  },
  "performance": {
    "avgExecutionTime": 95,
    "maxExecutionTime": 600,
    "successRate": 94.9
  },
  "topErrors": [
    {
      "message": "Timeout after 120s",
      "count": 3,
      "task": "deals-morning"
    },
    {
      "message": "API rate limit exceeded",
      "count": 2,
      "task": "tech-news-digest"
    }
  ]
}
```

---

## 🎯 **监控的 Cron Jobs**（14个）

| 任务 | 日志级别 | 监控重点 |
|------|---------|---------|
| Daily Auto-Update | INFO/ERROR | 执行状态 |
| Workspace Backup | INFO/ERROR | 备份状态 |
| Content Research | INFO/WARN | 性能 |
| Content Writing | INFO | 执行时间 |
| Content Thumbnails | INFO | 执行时间 |
| Deals Morning | ERROR/WARN | 超时/失败 |
| Deals Noon | ERROR/WARN | 超时/失败 |
| Deals Evening | ERROR/WARN | 超时/失败 |
| Tech News Digest | ERROR/WARN | API 失败 |
| Video Ideas Daily | INFO | 执行时间 |
| Earnings Calendar | INFO/ERROR | 执行状态 |
| Failure Monitor | INFO/ERROR | 监控状态 |
| Skill Sync | INFO/ERROR | 同步状态 |
| Cron Scheduler | INFO/ERROR | 调度状态 |

---

## 💡 **智能建议**

### **自动建议**（基于分析）

1. **超时优化**
   ```
   检测到: deals-morning 多次超时
   建议: 增加超时时间 120s → 300s
   ```

2. **性能优化**
   ```
   检测到: content-research 响应时间过长
   建议: 优化网络请求或增加缓存
   ```

3. **资源优化**
   ```
   检测到: 内存使用率过高
   建议: 增加内存或优化代码
   ```

---

## 📝 **更新日志**

### v1.0.0 (2026-03-12)
- ✅ 初始版本
- ✅ 日志监控
- ✅ 错误检测
- ✅ 模式分析
- ✅ 报告生成
- ✅ Discord 推送

---

**🚀 让你的日志分析更加智能和高效！**
