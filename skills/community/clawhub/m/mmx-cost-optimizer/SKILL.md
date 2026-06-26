---
name: cost-optimizer
description: 智能AI成本优化系统，集成Token预算管理、边际收益检测、多维度成本统计。当用户要求优化AI调用成本、控制Token使用、监控预算消耗、生成成本报告、降低API费用时使用。
---

# Cost Optimizer Pro

> 智能AI成本优化系统 - Claude Code成本管理核心技能提炼

## 核心能力

1. **Token预算管理** - 智能追踪、边际收益检测、自动决策
2. **多维度成本统计** - 输入/输出/缓存/搜索全维度
3. **实时成本监控** - 每轮显示、累计统计
4. **优化建议生成** - 基于使用模式自动建议

## 预算配置

```typescript
const BUDGET_CONFIG = {
  // 完成阈值
  completionThreshold: 0.9,

  // 边际收益递减检测
  diminishingThreshold: 500,

  // 最大继续次数
  maxContinuations: 10,

  // 警告阈值
  warningThreshold: 0.75,

  // 成本阈值
  costWarningThreshold: 1.00,
  costHardLimit: 10.00
}
```

## 决策算法

### 预算决策流程

```
检查Token使用
      ↓
是否 < 75% 预算？
  ├─ 是 → 正常继续
  ↓
是否 < 90% 预算？
  ├─ 是 → 继续 + nudgeMessage
  ↓
是否边际递减？
  ├─ 是 → 停止（边际收益递减）
  ↓
之前有继续吗？
  ├─ 是 → 停止（正常完成）
  └─ 否 → 继续等待
```

### 边际收益检测

```typescript
function isDiminishing(tracker, delta): boolean {
  return (
    tracker.continuationCount >= 3 &&
    delta < DIMINISHING_THRESHOLD &&
    tracker.lastDeltaTokens < DIMINISHING_THRESHOLD
  )
}
```

## 成本追踪

### Token类型

| 类型 | 典型成本 | 优化潜力 |
|-----|---------|---------|
| input_tokens | $3.5/1M | 高 |
| output_tokens | $15/1M | 中 |
| cache_read | ~10% input | 自动 |
| cache_creation | ~30% input | 一次性 |
| web_search | $0.01/次 | 按需 |

### 成本计算

```typescript
costUSD = inputTokens × inputPrice + outputTokens × outputPrice
```

## 使用示例

### 基本使用

```typescript
import { createBudgetTracker, checkTokenBudget } from './tokenBudget.js'

const tracker = createBudgetTracker()
const budget = 100000

function onAPIResponse(usage) {
  const totalTokens = usage.input_tokens + usage.output_tokens
  const decision = checkTokenBudget(tracker, budget, totalTokens)

  if (decision.action === 'continue') {
    console.log(decision.nudgeMessage)
  } else {
    console.log('停止原因:', decision.completionEvent)
  }
}
```

### 成本监控

```typescript
function formatTotalCost() {
  return `
Total cost:            ${formatCost(getTotalCostUSD())}
Total duration (API):  ${formatDuration(getTotalAPIDuration())}
Total code changes:    ${linesAdded} lines added, ${linesRemoved} removed
Usage by model:
  ${formatModelUsage()}
  `.trim()
}
```

## 优化策略

### 1. 缓存复用
- 相同上下文用cache_read
- 成本降低约90%

### 2. 上下文压缩
- 减少input_tokens
- 保留关键信息

### 3. 输出精简
- 减少output_tokens
- 避免冗长回复

### 4. 批量操作
- 减少API调用次数
- 合并相似任务

## 显示格式

```
Total cost:            $0.0234
Total duration (API):  45.2s
Total code changes:    127 lines added, 43 lines removed
Usage by model:
  claude-sonnet:  12,500 input, 3,200 output, 89 cache read ($0.0189)
  claude-haiku:   2,000 input, 800 output ($0.0045)
```

## 配置选项

| 参数 | 默认值 | 说明 |
|-----|-------|------|
| completionThreshold | 0.9 | 完成阈值 |
| diminishingThreshold | 500 | 边际收益阈值 |
| maxContinuations | 10 | 最大继续次数 |
| warningThreshold | 0.75 | 警告阈值 |

## 集成Hook

```typescript
// 压缩前Hook
registerHook('pre_compact', async (ctx) => {
  const costSavings = estimateCostSavings(ctx.messages)
  if (costSavings > 0.01) {
    ctx.modifiedStrategy = 'aggressive'
  }
})

// 压缩后Hook
registerHook('post_compact', async (ctx) => {
  logCostEvent('compact', {
    tokensBefore: ctx.tokensBefore,
    tokensAfter: ctx.tokensAfter,
    savings: estimateSavings(ctx)
  })
})
```

## 会话恢复

```typescript
// 保存会话成本
function saveCurrentSessionCosts() {
  saveCurrentProjectConfig(current => ({
    ...current,
    lastCost: getTotalCostUSD(),
    lastAPIDuration: getTotalAPIDuration(),
    lastTotalInputTokens: getTotalInputTokens(),
    lastTotalOutputTokens: getTotalOutputTokens(),
    lastModelUsage: getModelUsage(),
    lastSessionId: getSessionId()
  }))
}

// 恢复会话成本
function restoreCostStateForSession(sessionId) {
  const data = getStoredSessionCosts(sessionId)
  if (data && data.lastSessionId === sessionId) {
    setCostStateForRestore(data)
    return true
  }
  return false
}
```

## 优化建议生成

```typescript
function generateOptimizationSuggestions(usage, cost) {
  const suggestions = []

  // 检查缓存利用率
  const cacheHitRate = usage.cacheReadInputTokens / usage.inputTokens
  if (cacheHitRate < 0.3) {
    suggestions.push({
      type: 'cache',
      priority: 'high',
      message: '缓存命中率较低，考虑复用上下文',
      potential: '可节省30-50%成本'
    })
  }

  // 检查输出长度
  const outputRatio = usage.outputTokens / usage.inputTokens
  if (outputRatio > 0.5) {
    suggestions.push({
      type: 'output',
      priority: 'medium',
      message: '输出长度较高，考虑精简回复',
      potential: '可节省10-20%成本'
    })
  }

  return suggestions
}
```
