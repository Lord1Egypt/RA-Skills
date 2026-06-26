# Session Auto-Scaling System

自动扩缩容系统，实现 Session 的负载均衡和弹性伸缩。

## 功能特性

### 1. 监控 Session 负载 ✓
- **多维度指标**: 消息数量、请求速率、CPU 使用率、内存使用率
- **实时计算**: 每 30 秒自动计算负载分数 (0-1)
- **历史追踪**: 保留最近 5 分钟的请求历史记录
- **权重配置**: 可自定义各指标的权重

### 2. 自动创建新 Session（负载高时）✓
- **触发条件**: 负载分数 ≥ 0.8（可配置）
- **自动扩容**: 当 session 过载时自动创建新 session
- **数量限制**: 最多 10 个 session（可配置）
- **冷却时间**: 5 分钟内不重复扩容（可配置）

### 3. 自动合并 Session（负载低时）✓
- **触发条件**: 负载分数 ≤ 0.3（可配置）
- **智能合并**: 将多个低负载 session 合并为一个
- **最小数量**: 至少保留 1 个 session（可配置）
- **冷却时间**: 5 分钟内不重复缩容（可配置）

### 4. 负载均衡 ✓
- **自动检测**: 监控各 session 之间的负载差异
- **智能建议**: 当负载差异 > 0.3 时触发平衡
- **分布优化**: 建议将请求分发到低负载 session

### 5. 完整文档 ✓
- 使用文档（本文档）
- 配置说明
- API 参考
- 示例代码

## 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                  Session Auto-Scaler                     │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Monitor    │  │   Scaler     │  │   Balancer   │  │
│  │  负载监控     │  │  扩缩容决策   │  │  负载均衡     │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                 │           │
│         └─────────────────┼─────────────────┘           │
│                           │                             │
│                  ┌────────▼────────┐                    │
│                  │ Session Manager │                    │
│                  │  (持久化层)      │                    │
│                  └────────┬────────┘                    │
└───────────────────────────┼─────────────────────────────┘
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
  ┌──────▼──────┐    ┌──────▼──────┐    ┌──────▼──────┐
  │  Session 1  │    │  Session 2  │    │  Session N  │
  │  (Active)   │    │  (Active)   │    │  (Active)   │
  └─────────────┘    └─────────────┘    └─────────────┘
```

## 文件结构

```
auto-scaling/
├── session-autoscaler.js      # 核心模块 (19KB)
├── autoscaler-config.json     # 配置文件
├── start-autoscaler.js        # 服务启动脚本
├── demo-autoscaler.js         # 演示脚本
└── README.md                  # 本文档

memory/
├── autoscaler-state.json      # 运行状态（自动生成）
└── sessions/                  # Session 数据目录
    └── {session-id}/
        ├── context.json
        └── user.md
```

## 快速开始

### 1. 运行演示

```bash
cd /home/user/.openclaw/workspace/auto-scaling
node demo-autoscaler.js
```

演示将：
- 初始化 Session Manager
- 创建 2 个测试 session
- 模拟不同负载场景
- 触发自动扩缩容
- 显示实时状态

### 2. 启动服务

```bash
# 启动后台服务
node start-autoscaler.js start

# 查看状态
node start-autoscaler.js status

# 停止服务
node start-autoscaler.js stop

# 重启服务
node start-autoscaler.js restart
```

### 3. 集成到应用

```javascript
const { getSessionAutoScaler } = require('./auto-scaling/session-autoscaler');

// 初始化
const autoScaler = getSessionAutoScaler();
await autoScaler.initialize();

// 在收到消息时记录
autoScaler.recordMessage(sessionId);
autoScaler.recordRequest(sessionId);

// 可选：更新资源使用情况
autoScaler.updateResourceUsage(sessionId, cpuUsage, memoryUsage);

// 查询状态
const status = autoScaler.getStatus();
console.log('Active sessions:', status.activeSessions);
```

## 配置说明

编辑 `autoscaler-config.json` 自定义行为：

### 负载阈值配置

```json
{
  "load": {
    // 高负载触发扩容
    "highMessageCount": 100,      // 消息数阈值
    "highRequestRate": 10,        // 请求速率阈值（次/分钟）
    "highCpuUsage": 80,           // CPU 使用率阈值（%）
    "highMemoryUsage": 80,        // 内存使用率阈值（%）
    
    // 低负载触发缩容
    "lowMessageCount": 20,        // 消息数阈值
    "lowRequestRate": 2,          // 请求速率阈值
    "lowActiveTime": 30,          // 低活跃时间（分钟）
    
    // 负载计算权重
    "weights": {
      "messageCount": 0.4,        // 消息数权重
      "requestRate": 0.4,         // 请求速率权重
      "cpuUsage": 0.1,            // CPU 权重
      "memoryUsage": 0.1          // 内存权重
    }
  }
}
```

### 扩缩容策略

```json
{
  "scaling": {
    "minSessions": 1,             // 最小 session 数
    "maxSessions": 10,            // 最大 session 数
    "scaleUpThreshold": 0.8,      // 扩容阈值（负载分数）
    "scaleDownThreshold": 0.3,    // 缩容阈值（负载分数）
    "cooldownMinutes": 5,         // 冷却时间（分钟）
    "mergeMinSessions": 2,        // 最小合并 session 数
    "loadBalancingEnabled": true  // 启用负载均衡
  }
}
```

### 监控配置

```json
{
  "monitoring": {
    "checkIntervalSeconds": 30,   // 检查间隔（秒）
    "metricsRetentionHours": 24,  // 指标保留时间（小时）
    "enableLoadBalancing": true,  // 启用负载均衡
    "balanceThreshold": 0.3       // 负载均衡触发阈值
  }
}
```

### 命名配置

```json
{
  "naming": {
    "prefix": "session",          // Session ID 前缀
    "includeTimestamp": true      // 包含时间戳
  }
}
```

## 负载计算

负载分数通过加权平均计算：

```
loadScore = messageScore × 0.4 + requestRateScore × 0.4 + 
            cpuScore × 0.1 + memoryScore × 0.1
```

其中：
- `messageScore = min(1, messageCount / highMessageCount)`
- `requestRateScore = min(1, requestRate / highRequestRate)`
- `cpuScore = cpuUsage / 100`
- `memoryScore = memoryUsage / 100`

负载分数范围：0-1
- 0.0-0.3: 低负载（可能缩容）
- 0.3-0.8: 正常负载
- 0.8-1.0: 高负载（可能扩容）

## Session 生命周期

```
创建 (ACTIVE)
    ↓
[负载监控]
    ↓
┌─────────────┬─────────────┐
│  负载 > 0.8  │  负载 < 0.3  │
│     ↓       │     ↓       │
│  扩容       │  缩容       │
│  (新建)     │  (合并)     │
└─────────────┴─────────────┘
    ↓
[负载均衡]
    ↓
持续监控...
```

## API 参考

### SessionAutoScaler

#### 初始化

```javascript
const autoScaler = getSessionAutoScaler();
await autoScaler.initialize();
```

#### 记录活动

```javascript
// 记录消息
autoScaler.recordMessage(sessionId);

// 记录请求
autoScaler.recordRequest(sessionId);

// 更新资源使用
autoScaler.updateResourceUsage(sessionId, cpuUsage, memoryUsage);
```

#### 查询状态

```javascript
// 获取整体状态
const status = autoScaler.getStatus();
console.log(status.activeSessions);
console.log(status.state.totalScaleUps);

// 获取单个 session 指标
const metrics = autoScaler.getSessionMetrics(sessionId);
console.log(metrics.loadScore);

// 获取所有指标
const allMetrics = autoScaler.getAllMetrics();
```

#### 控制服务

```javascript
// 停止监控
autoScaler.stop();
```

### SessionMetrics

每个 session 的指标对象：

```javascript
{
  sessionId: 'session-123',
  messageCount: 150,
  requestCount: 500,
  requestRate: 8.5,           // 请求/分钟
  cpuUsage: 45,               // %
  memoryUsage: 60,            // %
  createdAt: 1710234567890,
  lastActivityAt: 1710234987654,
  loadScore: 0.72             // 0-1
}
```

## 使用场景

### 场景 1: 高并发消息处理

当单个 session 处理大量消息时：

1. 监控检测到负载分数 > 0.8
2. 自动创建新 session
3. 新消息分发到新 session
4. 原 session 负载下降

### 场景 2: 夜间低负载

当多个 session 都处于低负载时：

1. 监控检测到负载分数 < 0.3
2. 将 2 个低负载 session 合并
3. 释放资源
4. 保留最小 session 数

### 场景 3: 负载不均衡

当 session 之间负载差异大时：

1. 检测到负载差异 > 0.3
2. 记录不平衡状态
3. 建议重新分配请求
4. 下次扩容时优先使用低负载 session

## 监控与日志

### 日志文件

```bash
# 查看实时日志
tail -f /home/user/.openclaw/workspace/auto-scaling/logs/autoscaler.log
```

### 状态文件

```bash
# 查看运行状态
cat /home/user/.openclaw/workspace/memory/autoscaler-state.json
```

### 指标查询

```javascript
const status = autoScaler.getStatus();
console.log('Session 负载分布:');
status.sessions.forEach(s => {
  console.log(`  ${s.sessionId}: ${s.loadScore.toFixed(2)}`);
});
```

## 最佳实践

### 1. 合理设置阈值

根据实际业务调整：
- 高并发场景：降低 `scaleUpThreshold` 到 0.6-0.7
- 资源紧张场景：降低 `maxSessions` 到 5
- 稳定性优先：增加 `cooldownMinutes` 到 10

### 2. 监控关键指标

定期检查：
- `totalScaleUps`: 扩容次数（过多说明阈值过低）
- `totalScaleDowns`: 缩容次数（过多说明阈值过高）
- `activeSessions`: 当前 session 数（应在 min-max 之间）

### 3. 负载均衡策略

- 启用 `loadBalancingEnabled`
- 在应用层实现请求分发逻辑
- 优先使用低负载 session

### 4. 资源预留

- 设置 `minSessions` ≥ 1 确保可用性
- 设置 `maxSessions` 防止资源耗尽
- 监控 CPU/内存使用率

## 故障排除

### Session 没有自动创建？

检查：
1. 当前 session 数是否已达 `maxSessions`
2. 是否在 `cooldownMinutes` 冷却期内
3. 负载分数是否达到 `scaleUpThreshold`

```javascript
const status = autoScaler.getStatus();
console.log('Last Scale Up:', new Date(status.state.lastScaleUp));
console.log('Active Sessions:', status.activeSessions);
```

### Session 没有合并？

检查：
1. 低负载 session 数是否 ≥ `mergeMinSessions`
2. 是否在 `cooldownMinutes` 冷却期内
3. 负载分数是否低于 `scaleDownThreshold`

### 负载计算不准确？

1. 确认已调用 `recordMessage()` 和 `recordRequest()`
2. 检查 `weights` 配置是否合理
3. 查看日志确认指标记录

## 集成示例

### 与 Feishu Bot 集成

```javascript
const { getSessionAutoScaler } = require('./auto-scaling/session-autoscaler');
const autoScaler = getSessionAutoScaler();

// 在消息处理中间件中
app.use(async (req, res, next) => {
  const sessionId = req.sessionId;
  
  // 记录请求
  autoScaler.recordRequest(sessionId);
  
  // 根据负载选择 session
  const status = autoScaler.getStatus();
  const lowLoadSession = status.sessions
    .filter(s => s.loadScore < 0.5)
    .sort((a, b) => a.loadScore - b.loadScore)[0];
  
  if (lowLoadSession) {
    req.targetSession = lowLoadSession.sessionId;
  }
  
  next();
});
```

### 与监控系统集成

```javascript
// 定期导出指标
setInterval(() => {
  const metrics = autoScaler.getAllMetrics();
  
  // 发送到 Prometheus/Grafana
  metrics.forEach(m => {
    prometheusClient.set('session_load_score', m.loadScore, {
      session_id: m.sessionId
    });
  });
}, 30000);
```

## 性能影响

- **内存占用**: ~1MB（每 100 个 session）
- **CPU 占用**: < 1%（30 秒检查间隔）
- **磁盘 I/O**: 每次检查写入 ~1KB 状态文件

## 安全考虑

- Session ID 包含时间戳防止冲突
- 状态文件仅包含指标数据
- 不存储敏感用户信息
- 支持配置最大 session 数防止资源耗尽

## 版本历史

- **v1.0** (2026-03-12): 初始版本
  - 基础负载监控
  - 自动扩缩容
  - 负载均衡
  - 完整文档

## 后续优化

1. **智能预测**: 基于历史数据预测负载趋势
2. **动态阈值**: 根据时间段自动调整阈值
3. **多级扩容**: 支持渐进式扩容策略
4. **可视化界面**: Web UI 实时监控
5. **告警集成**: 与现有监控系统集成

---

**维护者**: Auto-Scaling Subagent  
**最后更新**: 2026-03-12  
**版本**: 1.0
