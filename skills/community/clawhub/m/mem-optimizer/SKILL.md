---
name: MemOptimizer (记忆优化器)
slug: mem-optimizer
version: 1.2.0
description: "记忆优化与压缩工具。结合 self-improving 机制，自动统计、压缩和优化记忆文件，减少 token 消耗。支持多智能体优化和24小时工作检测。触发关键词：优化记忆、记忆优化、总结你自己、MemOptimizer、memopt、执行多智能体记忆优化流程"
changelog: |
  v1.2.0 - 新增多智能体优化功能，支持24小时工作检测，生成详细报告
  v1.1.0 - 整合 self-improving 反思机制，支持每日定时任务
metadata:
  openclaw:
    global: true
    requires:
      bins: []
    triggers:
      - "优化记忆"
      - "记忆优化"
      - "总结你自己"
      - "MemOptimizer"
      - "memopt"
      - "执行记忆优化流程"
      - "执行多智能体记忆优化流程"
    tools:
      - mem_optimize
      - mem_stats
    cron:
      - expression: "0 8 * * *"
        action: "mem_optimize_daily"
        description: "每天上午 8 点执行记忆优化并发送每日总结"
---

# MemOptimizer (记忆优化器) 🧠

**记忆压缩与统计工具 - 整合 Self-Improving 机制**

自动扫描工作区的 memory 文件，统计 tokens 使用情况，执行压缩优化，并结合自我反思机制持续改进优化策略。

## 触发方式

### 手动触发
当用户说出以下关键词时自动激活：
- 优化记忆
- 记忆优化  
- 总结你自己
- MemOptimizer
- memopt

### 自动触发
- **每日定时**：每天上午 8:00 自动执行（UTC 时间）
- 执行后自动发送每日总结报告

## 核心功能

### 1. Token 统计与压缩
- 扫描 `memory/` 目录下所有 `.md` 文件
- 估算每个文件的 token 消耗（中文 2 字符/token，英文 4 字符/token）
- 自动识别冗长的记忆条目（>50 行）
- 生成摘要，保留关键信息

### 2. Self-Improving 整合 🆕
结合自我反思机制，持续优化记忆策略：

#### 反思触发条件
| 触发场景 | 置信度 | 动作 |
|---------|--------|------|
| 用户指出"这个压缩太过了" | 高 | 记录到 `corrections.md` |
| 用户说"保留更多细节" | 高 | 调整压缩阈值 |
| 多次压缩后用户要求恢复 | 中 | 标记为"过度压缩"模式 |
| 用户确认"这样压缩很好" | 中 | 推广为全局偏好 |

#### 反思日志格式
```markdown
## [Date] — Memory Optimization

**What I did:** Compressed 3 memory files, freed 2500 tokens
**Outcome:** User approved the compression
**Reflection:** Compression ratio of 40% was well received
**Lesson:** 40-50% compression ratio is safe for daily notes
**Status:** ✅ promoted to global preferences
```

#### 学习演化路径
1. **Tentative** — 单次优化后观察用户反馈
2. **Emerging** — 2 次相似反馈，可能模式
3. **Pending** — 3 次反馈，请求确认
4. **Confirmed** — 用户确认，永久偏好
5. **Archived** — 90 天未使用，保留但停用

### 3. 每日总结报告（自动）
每天上午 8 点自动执行，包含：

#### 报告内容
- **记忆优化结果**
  - 释放的 tokens 数量
  - 总结的 tokens 数量
  - 处理的文件列表
  
- **服务器状态**
  - CPU/内存使用率
  - 磁盘空间
  - 网络状态
  
- **多智能体状态**
  - 活跃子 agent 列表
  - 各 agent 任务进度
  - 异常或警告
  
- **任务概览**
  - 过去 24 小时执行的任务
  - 成功/失败统计
  - 耗时最长的任务

#### 发送方式
- 通过 Feishu 发送给用户
- 包含可交互的卡片（如平台支持）
- 附带详细日志文件链接

## 工具使用

### mem_optimize - 执行记忆优化

```javascript
mem_optimize({
  dryRun: true,        // true=仅预览（默认）
  includeReflection: true,  // 是否记录反思（默认 true）
  compressionRatio: 0.4   // 目标压缩比（0-1）
})
```

**返回格式：**
```json
{
  "status": "success",
  "message": "已释放 1234 tokens，总结了 5678 tokens 记忆",
  "stats": {
    "freedTokens": 1234,
    "summarizedTokens": 5678,
    "filesProcessed": 5,
    "totalTokens": 15000,
    "compressionRatio": 0.42
  },
  "reflection": {
    "logged": true,
    "pattern": "compression_acceptable",
    "confidence": "medium"
  },
  "dryRun": true
}
```

### mem_stats - 统计记忆使用情况

```javascript
mem_stats()
```

**返回格式：**
```json
{
  "status": "success",
  "totalFiles": 10,
  "totalTokens": 15000,
  "files": [
    {
      "name": "2026-03-12.md",
      "tokens": 500,
      "lines": 45
    }
  ]
}
```

### mem_optimize_daily - 每日自动执行（内部工具）

由 cron 自动调用，执行完整优化并发送报告。

## 每日总结报告模板

```
🧠 每日记忆优化报告 - [日期]

📊 记忆优化结果
─────────────────────
• 释放 tokens: 1,234
• 总结 tokens: 5,678
• 处理文件：5 个
• 压缩率：42%

🖥️ 服务器状态
─────────────────────
• CPU: 23% (avg)
• 内存：4.2GB / 16GB
• 磁盘：45GB / 500GB
• 网络：正常

🤖 多智能体状态
─────────────────────
• 活跃子 agent: 2
  - mem-optimizer (完成)
  - web-search (进行中)
• 无异常警告

📋 任务概览 (过去 24h)
─────────────────────
• 总任务：12
• 成功：11
• 失败：1
• 平均耗时：2.3s

📝 反思日志
─────────────────────
• 新增学习：1 条
• 确认偏好：0 条
• 归档旧模式：0 条

[查看详细日志]
```

## 优化策略

### 压缩阈值
- **默认**：50 行以上开始压缩
- **可调整**：根据用户反馈动态调整
- **安全边界**：保留标题和前 20 行

### 安全机制
- **默认 dryRun**：仅预览不修改
- **用户确认**：执行实际压缩需确认
- **备份建议**：重要文件建议先备份
- **可恢复**：压缩内容可手动恢复

### Self-Improving 循环
```
1. 执行优化
   ↓
2. 观察用户反馈
   ↓
3. 记录到 reflections.md
   ↓
4. 模式累积（3 次）
   ↓
5. 请求确认
   ↓
6. 更新全局偏好
   ↓
7. 下次优化应用新策略
```

## 与 memory-qdrant 的协同

- **memory-qdrant**：向量数据库，用于语义搜索和长期记忆存储
- **MemOptimizer**：文件压缩工具，减少 memory 文件的 token 消耗

两者互补：
- qdrant 处理语义记忆
- MemOptimizer 处理文件存储优化
- 优化结果同步到 qdrant 用于长期学习

## 配置选项

可通过环境变量或配置文件自定义：

```javascript
{
  "compressionThreshold": 50,    // 压缩阈值（行数）
  "maxSummaryLines": 20,         // 摘要最大行数
  "defaultDryRun": true,         // 默认预览模式
  "targetCompressionRatio": 0.4, // 目标压缩比
  "excludePatterns": [],         // 排除的文件模式
  "reflectionEnabled": true,     // 是否启用反思
  "dailyReportTime": "08:00"     // 每日报告时间（UTC）
}
```

## 定时任务配置

### 自动执行时间
- **时间**：每天上午 8:00（UTC）
- **时区**：UTC（可根据需要调整）

### 配置位置
```yaml
# ~/.openclaw/config.yaml 或 agent 配置
cron:
  - expression: "0 8 * * *"
    action: "mem_optimize_daily"
    enabled: true
```

### 禁用方法
如功能带来负担，可：
1. 编辑配置，设置 `enabled: false`
2. 或删除 cron 配置项
3. 或删除整个 skill 目录

## 未来扩展

- [ ] 支持智能去重（语义相似度检测）
- [ ] 支持自动归档（30 天前的文件）
- [ ] 支持记忆导出/导入
- [ ] 支持记忆分类标签
- [ ] 支持多时区报告时间
- [ ] 支持报告模板自定义
