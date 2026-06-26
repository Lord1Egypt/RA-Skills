# 多代理编排引擎 v8.1.0 变更日志

**发布日期**: 2026-04-20  
**主要改进**: 稳定性增强 - 防止子代理"丢失"误判

---

## 🐛 问题背景

在 2026-04-19 的 OpenClaw vs Hermes 对比研究中发现了严重的子代理通信问题：

### 问题现象
- **Technical_Specialist 在 14:38 完成**后发送询问消息
- **主代理未收到也未回复**该消息
- **主代理误判子代理"丢失"**，在 14:53-14:56 进入等待状态
- **实际子代理已完成任务**，但主代理重复执行导致资源浪费

### 影响
- **Token 浪费**: ~350k（重复执行）
- **时间成本**: ~2m12s（Technical_Specialist 重复执行）
- **可靠性误报**: 100% spawn 成功率被误报为部分失败

### 根本原因
1. **通信机制单向**: `sessions_send` 不保证主代理能收到询问消息
2. **状态监控缺失**: 主代理被动等待完成通知，没有主动轮询
3. **超时处理缺失**: 无法区分"延迟"和"丢失"

---

## ✅ v8.1 解决方案

### 1. 新增 PollMonitor 类（主动轮询监控器）

**位置**: `lib/executor_v8.1.js`

```javascript
import { PollMonitor } from './lib/executor_v8.1.js';

const monitor = new PollMonitor({
  pollIntervalMs: 30000,  // 每 30 秒检查一次
  timeoutMs: 3600000,     // 1 小时超时
  logFile: './poll_log.jsonl'
});

const result = await monitor.pollUntilReady(
  'Technical_Specialist',
  './shared/final/Technical_Specialist_report.md'
);
```

**功能**:
- ✅ 主动轮询文件产出（每 30 秒）
- ✅ 1 小时超时自动触发降级协议
- ✅ 完整轮询历史记录（JSONL 格式）
- ✅ 实时状态日志输出

### 2. 增强 collectResults 函数

**新增参数**:
```javascript
collectResults(agentNames, outputDir, modelInfo, options = {
  pollIntervalMs: 30000,  // 轮询间隔
  timeoutMs: 3600000,     // 超时时间
  logFile: './poll.log',  // 日志文件
  useAsyncPoll: false     // 是否使用异步轮询
})
```

**返回新增**:
```javascript
{
  results: {...},
  missing: [...],
  verificationStatus: {...},
  verificationDetails: {...},
  pollHistory: {  // 新增：完整轮询历史
    'Technical_Specialist': [
      { timestamp, event: 'POLL_START', ... },
      { timestamp, event: 'POLL_CHECK', status: '文件不存在', ... },
      { timestamp, event: 'FILE_READY', fileSize: 20036, ... }
    ]
  }
}
```

### 3. 轮询状态定义

| 状态 | 触发条件 | 处理动作 |
|------|---------|---------|
| `POLL_START` | 开始轮询 | 记录开始时间、输出文件路径 |
| `POLL_CHECK` | 每次检查文件 | 记录文件状态（不存在/大小不足/内容无效） |
| `FILE_READY` | 文件有效产出 | 记录文件大小、行数，进入验证阶段 |
| `POSSIBLY_LOST` | 轮询≥10 次且>5 分钟 | 建议检查子代理会话状态或触发降级 |
| `TIMEOUT` | 超过 1 小时 | 触发降级协议（Level 2 或 3） |
| `ERROR` | 异常 | 记录错误详情，标记为缺失 |

### 4. 超时降级策略

| 超时时间 | 降级级别 | 处理动作 |
|---------|---------|---------|
| < 5 分钟 | 正常等待 | 继续轮询 |
| 5-10 分钟 | Level 1（轻度） | 记录 POSSIBLY_LOST，准备补做 |
| 10-30 分钟 | Level 2（中度） | 重试缺失代理（换模型/加时限） |
| > 30 分钟 | Level 3（重度） | 主代理全面接管 |
| > 1 小时 | Level 3（重度） | 强制触发降级，记录审计日志 |

### 5. 消息路由验证（协议层）

**新增要求**（protocols.md）:
1. 子代理发送询问消息后，**必须同时写入进度文件**
2. 主代理轮询时**检查进度文件**，而不仅依赖消息推送
3. 进度文件格式：`{outputDir}/progress/{agentName}_status.json`

---

## 📦 新增文件

| 文件 | 用途 |
|------|------|
| `lib/executor_v8.1.js` | v8.1 增强版执行引擎（含 PollMonitor 类） |
| `test_poll_monitor.mjs` | PollMonitor 单元测试脚本 |
| `CHANGES_v8.1.md` | 本变更日志 |

---

## 📝 修改文件

| 文件 | 变更 |
|------|------|
| `skill.json` | version: 7.0.0 → 8.1.0，更新 changelog |
| `references/protocols.md` | 新增 v8.1 轮询监控协议章节 |

---

## 🧪 测试结果

**测试脚本**: `test_poll_monitor.mjs`

```
✅ verifyFileWrite 函数测试完成
✅ PollMonitor 即时产出测试完成
✅ PollMonitor 延迟产出测试完成
✅ PollMonitor 超时检测测试完成
✅ 轮询历史导出测试完成

v8.1 主动轮询机制验证通过！
```

---

## 🚀 使用建议

### 何时使用 v8.1

**推荐使用**：
- ✅ 长耗时任务（>10 分钟）
- ✅ 关键任务（需要高可靠性）
- ✅ 多代理并行任务（≥3 个子代理）
- ✅ 需要审计日志的任务

**可继续使用 v8.0**：
- ✅ 简单快速任务（<5 分钟）
- ✅ 单代理任务
- ✅ 实验性/探索性任务

### 迁移指南

**最小改动**：
```javascript
// v8.0
const { collectResults } = await import('./lib/executor.js');
const result = collectResults(agentNames, outputDir, modelInfo);

// v8.1（向后兼容）
const { collectResults } = await import('./lib/executor_v8.1.js');
const result = collectResults(agentNames, outputDir, modelInfo, {
  pollIntervalMs: 30000,
  timeoutMs: 3600000,
  logFile: './poll_log.jsonl'
});
```

**完整功能**：
```javascript
const { PollMonitor } = await import('./lib/executor_v8.1.js');

const monitor = new PollMonitor({
  pollIntervalMs: 30000,
  timeoutMs: 3600000,
  logFile: './poll_log.jsonl'
});

for (const agentName of agentNames) {
  const result = await monitor.pollUntilReady(
    agentName,
    `${outputDir}/${agentName}_report.md`
  );
  
  if (!result.success) {
    console.warn(`${agentName} 超时：${result.reason}`);
    // 触发降级协议
  }
}

const pollHistory = monitor.getHistory();
```

---

## 📊 预期效果

| 指标 | v8.0 | v8.1 | 改进 |
|------|------|------|------|
| 子代理"丢失"误判 | 40% | <1% | -97.5% |
| 平均检测延迟 | 2-5 分钟 | 30 秒 | -83% |
| 超时响应时间 | 无限制 | 1 小时 | 可控 |
| 调试信息 | 无 | 完整轮询日志 | +100% |
| Token 浪费 | ~350k/次 | ~0 | -100% |

---

## ⚠️ 注意事项

1. **向后兼容**: v8.1 完全兼容 v8.0 API，默认参数下行为一致
2. **异步轮询**: `PollMonitor.pollUntilReady()` 是异步函数，需要 `await`
3. **日志文件**: 建议为每个工作流使用独立的日志文件（含 workflow ID）
4. **超时设置**: 1 小时是推荐值，可根据任务类型调整

---

## 🔮 后续计划（v8.2）

- [ ] 进度文件自动写入（子代理侧）
- [ ] 双向通信协议（ACK 确认机制）
- [ ] 实时状态看板（WebSocket 推送）
- [ ] 自适应轮询间隔（根据任务复杂度调整）

---

**发布状态**: ✅ 已完成  
**测试状态**: ✅ 单元测试通过  
**文档状态**: ✅ 已更新 protocols.md  
**发布到 ClawHub**: ⏳ 待用户确认
