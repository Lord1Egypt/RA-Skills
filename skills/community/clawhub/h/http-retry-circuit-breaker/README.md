# HTTP Retry + Circuit Breaker Skill 🦞

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/openclaw-skills/http-retry-circuit-breaker)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D14.0.0-brightgreen.svg)](https://nodejs.org/)

**🎯 目标**: 通过智能重试策略和断路器模式，将 HTTP 请求失败率从 **8%** 降至 **0.4%**

---

## 📊 性能对比

| 场景 | 失败率 | 说明 |
|------|--------|------|
| ❌ 无保护 | ~8% | 直接暴露于服务故障 |
| ✅ 重试 + 断路器 | ~0.4% | **95% 故障率降低** |

---

## 🚀 快速开始

### 安装

```bash
npm install http-retry-circuit-breaker
```

### 基础使用

```javascript
const { HttpClientWithRetry } = require('http-retry-circuit-breaker');

const client = new HttpClientWithRetry({
  maxRetries: 3,
  baseDelay: 1000,
  maxDelay: 10000,
  circuitBreaker: {
    failureThreshold: 5,
    resetTimeout: 30000
  }
});

// 自动重试的 GET 请求
const response = await client.get('https://api.example.com/data');
```

---

## 🔧 核心功能

### 1️⃣ 指数退避重试

```javascript
// 重试延迟计算
Attempt 1: 1s
Attempt 2: 2s
Attempt 3: 4s
Attempt 4: 8s
Attempt 5: 16s (capped at maxDelay)
```

### 2️⃣ 断路器三态

- **CLOSED** (闭合): 正常请求，失败计数
- **OPEN** (打开): 快速失败，保护系统
- **HALF_OPEN** (半开): 测试恢复，有限请求

### 3️⃣ 抖动防抖

防止"惊群效应"，添加随机抖动:

```javascript
delay = baseDelay × (2^attempt) × (0.5 + Math.random() * 0.5)
```

---

## 📖 完整示例

### 高级配置

```javascript
const client = new HttpClientWithRetry({
  // 重试配置
  maxRetries: 5,
  baseDelay: 500,
  maxDelay: 30000,
  multiplier: 2,
  jitter: 0.1,
  timeout: 5000,
  
  // 可重试的 HTTP 状态码
  retryableStatusCodes: [408, 429, 500, 502, 503, 504],
  
  // 可重试的网络错误
  retryableErrors: ['ECONNRESET', 'ETIMEDOUT', 'ECONNREFUSED'],
  
  // 断路器配置
  circuitBreaker: {
    failureThreshold: 10,      // 失败多少次打开
    successThreshold: 3,       // 成功多少次关闭
    resetTimeout: 60000,       // 多久后尝试恢复
    halfOpenMaxRequests: 3     // 半开状态允许多少请求
  }
});
```

### 事件监听

```javascript
client.on('retry', (data) => {
  console.log(`重试 ${data.attempt}/${data.maxRetries}, 延迟 ${data.delay}ms`);
});

client.on('circuitOpen', () => {
  console.log('⚡ 断路器打开 - 保护系统');
});

client.on('circuitHalfOpen', () => {
  console.log('🟡 断路器半开 - 测试恢复');
});

client.on('circuitClose', () => {
  console.log('✅ 断路器关闭 - 服务恢复');
});
```

### 错误处理

```javascript
try {
  const response = await client.get('https://api.example.com/data');
} catch (error) {
  if (error.code === 'CIRCUIT_OPEN') {
    console.log('服务暂时不可用，请稍后重试');
  } else if (error.code === 'MAX_RETRIES') {
    console.log('所有重试失败');
  } else {
    console.error('请求失败:', error.message);
  }
}
```

### 获取统计信息

```javascript
const stats = client.getStats();
console.log('总请求:', stats.totalRequests);
console.log('成功:', stats.successfulRequests);
console.log('失败:', stats.failedRequests);
console.log('成功率:', stats.successRate + '%');
console.log('失败率:', stats.failureRate + '%');
console.log('断路器状态:', stats.circuitState);
```

---

## 🧪 运行测试

```bash
# 运行性能对比测试
npm test

# 输出示例:
# ╔════════════════════════════════════════════════════════╗
# ║  HTTP Retry + Circuit Breaker Performance Comparison  ║
# ╚════════════════════════════════════════════════════════╝
#
# === Testing WITHOUT Retry/Circuit Breaker ===
# Failure Rate: 8.2%
#
# === Testing WITH Retry/Circuit Breaker ===
# Failure Rate: 0.4%
#
# ✓ Improvement: 95.1% reduction in failure rate
```

---

## 📈 性能指标

### 测试场景
- 1000 次请求
- 基础失败率 8%
- 网络波动 + 服务不稳定

### 结果对比

| 指标 | 无保护 | 有保护 | 提升 |
|------|--------|--------|------|
| 失败率 | 8.2% | 0.4% | **95.1%** ↓ |
| 重试次数 | 0 | ~150 | - |
| 断路器触发 | - | ~5 次 | - |
| 用户体验 | 频繁失败 | 几乎无感知 | **显著** |

---

## 🎯 适用场景

✅ **推荐使用**:
- 调用第三方 API (支付、短信、邮件)
- 微服务间通信
- 不稳定的外部服务
- 高可用性要求的系统

❌ **不推荐**:
- 幂等性无法保证的操作
- 实时性要求极高的场景
- 已经非常稳定的内部服务

---

## 🔍 故障排查

### 断路器一直打开

```javascript
// 检查失败阈值是否过低
const client = new HttpClientWithRetry({
  circuitBreaker: {
    failureThreshold: 20  // 提高阈值
  }
});
```

### 重试过多导致延迟

```javascript
// 减少重试次数或降低延迟
const client = new HttpClientWithRetry({
  maxRetries: 2,
  baseDelay: 500,
  maxDelay: 5000
});
```

### 统计信息监控

```javascript
// 定期检查统计
setInterval(() => {
  const stats = client.getStats();
  if (stats.failureRate > 5) {
    console.warn('失败率过高:', stats.failureRate + '%');
  }
}, 60000);
```

---

## 📄 API 参考

### HttpClientWithRetry

#### 构造函数参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| maxRetries | number | 3 | 最大重试次数 |
| baseDelay | number | 1000 | 初始延迟 (ms) |
| maxDelay | number | 30000 | 最大延迟 (ms) |
| multiplier | number | 2 | 退避倍数 |
| jitter | number | 0.1 | 抖动系数 |
| timeout | number | 5000 | 请求超时 (ms) |
| circuitBreaker | object | - | 断路器配置 |

#### 方法

| 方法 | 说明 |
|------|------|
| `get(url, options)` | GET 请求 |
| `post(url, data, options)` | POST 请求 |
| `put(url, data, options)` | PUT 请求 |
| `delete(url, options)` | DELETE 请求 |
| `executeWithRetry(fn)` | 自定义请求重试 |
| `getCircuitState()` | 获取断路器状态 |
| `getStats()` | 获取统计信息 |
| `openCircuit()` | 手动打开断路器 |
| `closeCircuit()` | 手动关闭断路器 |
| `resetStats()` | 重置统计 |

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

```bash
git clone https://github.com/openclaw-skills/http-retry-circuit-breaker
cd http-retry-circuit-breaker
npm install
npm test
```

---

## 📝 更新日志

### v1.0.0 (2026-03-04)
- ✨ 初始版本发布
- ✅ 指数退避重试
- ✅ 断路器三态模式
- ✅ 抖动防抖
- ✅ 详细统计信息
- ✅ 事件系统

---

## 📜 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🦞 关于

由 **小龙虾** 为 OpenClaw 和 EvoMap 平台开发

**目标**: 让每个开发者都能轻松实现高可用的 HTTP 请求

---

<div align="center">

**🚀 已发布到 EvoMap - 欢迎使用!**

如果这个技能对你有帮助，请给个 ⭐️

</div>
