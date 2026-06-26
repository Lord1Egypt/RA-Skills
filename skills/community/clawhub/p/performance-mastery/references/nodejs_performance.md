# Node.js 性能分析与优化指南

## 目录
1. [1. 分析工具](#1-分析工具)
2. [2. V8 引擎与内存管理](#2-v8-引擎与内存管理)
3. [3. GC 调优](#3-gc-调优)
4. [4. 内存泄漏排查](#4-内存泄漏排查)
5. [5. 事件循环优化](#5-事件循环优化)
6. [6. 优化模式](#6-优化模式)
7. [7. HTTP/网络优化](#7-http网络优化)
8. [8. APM 与监控](#8-apm-与监控)
9. [9. 常见问题速查](#9-常见问题速查)

---

## 1. 分析工具

```bash
# Node.js 内置 profiler
node --prof app.js
node --prof-process isolate-*.log > profile.txt

# Chrome DevTools（推荐交互式分析）
node --inspect app.js
# 打开 chrome://inspect 连接

# clinic.js（最推荐，自动诊断）
npx clinic doctor -- node app.js       # 自动诊断瓶颈类型
npx clinic flame -- node app.js        # CPU 火焰图
npx clinic bubbleprof -- node app.js   # I/O 异步分析
npx clinic heapprofiler -- node app.js # 堆内存分析

# 0x 火焰图
npx 0x app.js

# autocannon（HTTP 压测）
npx autocannon -c 100 -d 30 http://localhost:3000
```

---

## 2. V8 引擎与内存管理

### V8 内存结构

```text
V8 堆内存
├── 新生代（Young Generation）— 短生命周期对象
│   ├── Semi-space From（活跃区）
│   └── Semi-space To（GC 时交换）
├── 老生代（Old Generation）— 长生命周期对象
│   ├── Old Pointer Space（含指针的对象）
│   └── Old Data Space（纯数据对象）
├── 大对象空间（Large Object Space）— > 页大小的对象
├── 代码空间（Code Space）— JIT 编译后的代码
└── Map Space — Hidden Class / Map 对象
```

### 关键内存参数

```bash
# 查看默认堆大小（64 位系统通常 ~1.5GB）
node -e "console.log(v8.getHeapStatistics())"

# 调整最大堆内存（OOM 时首先考虑）
node --max-old-space-size=4096 app.js    # 设为 4GB
node --max-semi-space-size=64 app.js     # 新生代半空间 64MB（默认 16MB）

# 查看内存使用
node -e "
const m = process.memoryUsage();
console.log({
  rss: (m.rss / 1024 / 1024).toFixed(1) + 'MB',
  heapTotal: (m.heapTotal / 1024 / 1024).toFixed(1) + 'MB',
  heapUsed: (m.heapUsed / 1024 / 1024).toFixed(1) + 'MB',
  external: (m.external / 1024 / 1024).toFixed(1) + 'MB',
  arrayBuffers: (m.arrayBuffers / 1024 / 1024).toFixed(1) + 'MB'
});
"
```

### V8 优化杀手（Deoptimization）

```javascript
// ❌ 避免：改变对象形状（Hidden Class 变化）
const obj = {};
obj.a = 1;
obj.b = 2;  // 每次添加属性都会创建新 Hidden Class

// ✅ 推荐：预先定义所有属性
const obj = { a: 1, b: 2 };

// ❌ 避免：delete 操作符（触发去优化）
delete obj.prop;

// ✅ 推荐：设为 undefined
obj.prop = undefined;

// ❌ 避免：try-catch 包裹大段代码（阻止优化）
// ✅ 推荐：只包裹可能抛异常的最小代码段

// ❌ 避免：混合类型数组
const arr = [1, 'two', 3.0, null];  // V8 退化为通用数组

// ✅ 推荐：保持类型一致
const nums = [1, 2, 3, 4];  // V8 使用 SMI 或 Double 数组
```

---

## 3. GC 调优

### GC 类型

| GC 类型 | 作用域 | STW 时间 | 触发条件 |
|---------|--------|----------|----------|
| Scavenge | 新生代 | 1-5ms | 新生代半空间满 |
| Mark-Sweep | 老生代 | 10-100ms+ | 老生代空间不足 |
| Mark-Compact | 老生代 | 较长 | 老生代碎片化严重 |
| Incremental Marking | 老生代 | 分步 | 渐进式标记 |

### GC 诊断命令

```bash
# 输出 GC 日志
node --trace-gc app.js
# 输出示例: [12345:0x...] 42 ms: Scavenge 8.2 (10.0) -> 4.1 (10.0) MB, 1.2 / 0.0 ms

# 详细 GC 日志
node --trace-gc --trace-gc-verbose app.js

# 暴露 GC 手动触发（仅调试用）
node --expose-gc -e "global.gc(); console.log(process.memoryUsage())"

# 限制 GC 暂停时间（实验性）
node --max-old-space-size=4096 --optimize-for-size app.js
```

### GC 优化策略

```javascript
// 1. 减少短生命周期对象分配
// ❌ 每次请求创建新对象
app.get('/', (req, res) => {
  const config = { timeout: 5000, retries: 3 };  // 每次请求都分配
});

// ✅ 复用对象
const CONFIG = Object.freeze({ timeout: 5000, retries: 3 });
app.get('/', (req, res) => {
  // 直接使用 CONFIG
});

// 2. 对象池模式
class ObjectPool {
  constructor(factory, size = 100) {
    this.factory = factory;
    this.pool = Array.from({ length: size }, factory);
  }
  acquire() { return this.pool.pop() || this.factory(); }
  release(obj) { this.pool.push(obj); }
}

// 3. Buffer 复用
const bufferPool = Buffer.allocUnsafe(64 * 1024);  // 预分配
// 而非每次 Buffer.alloc(64 * 1024)
```

---

## 4. 内存泄漏排查

### 常见泄漏源

```javascript
// 1. 事件监听器未清理
emitter.on('data', handler);  // 累积
// 修复：
emitter.removeListener('data', handler);
// 或使用 once：
emitter.once('data', handler);

// 2. 闭包引用
function createLeak() {
  const bigData = new Array(1000000).fill('x');
  return function() {
    // bigData 被闭包引用，永远不会被 GC
    console.log(bigData.length);
  };
}

// 3. 全局缓存无上限
const cache = {};
function addToCache(key, value) {
  cache[key] = value;  // 永远增长
}
// 修复：使用 LRU 缓存
const LRU = require('lru-cache');
const cache = new LRU({ max: 500, ttl: 1000 * 60 * 5 });

// 4. 定时器未清理
const timer = setInterval(() => { /* ... */ }, 1000);
// 修复：
clearInterval(timer);

// 5. Promise 未处理
async function leak() {
  const promises = [];
  for (let i = 0; i < 100000; i++) {
    promises.push(fetch(url));  // 大量 pending Promise
  }
  // 修复：限制并发
}
```

### 排查工具

```bash
# heapdump 快照对比（生产环境推荐）
npm install heapdump
# 代码中：
# require('heapdump');
# kill -USR2 <pid>  → 生成 heapdump-*.heapsnapshot

# 使用 Chrome DevTools 对比两个快照
# Memory → Load → Comparison 视图

# 使用 memwatch-next 自动检测
npm install @airbnb/node-memwatch
# const memwatch = require('@airbnb/node-memwatch');
# memwatch.on('leak', (info) => console.log('Leak:', info));

# 进程级内存监控
node -e "
setInterval(() => {
  const m = process.memoryUsage();
  console.log(new Date().toISOString(),
    'RSS:', (m.rss/1024/1024).toFixed(1)+'MB',
    'Heap:', (m.heapUsed/1024/1024).toFixed(1)+'MB');
}, 5000);
"
```

---

## 5. 事件循环优化

### 事件循环阶段

```text
   ┌───────────────────────────┐
┌─>│         timers             │  setTimeout / setInterval
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │     pending callbacks      │  I/O 回调
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │       idle, prepare        │  内部使用
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │         poll               │  新 I/O 事件（最重要）
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │         check              │  setImmediate
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │    close callbacks         │  socket.on('close')
│  └─────────────┬─────────────┘
└─────────────────┘
```

### 监控事件循环延迟

```javascript
// 方法 1: monitorEventLoopDelay（Node.js >= 11.10）
const { monitorEventLoopDelay } = require('perf_hooks');
const h = monitorEventLoopDelay({ resolution: 20 });
h.enable();
setInterval(() => {
  console.log(`EL delay: min=${h.min/1e6}ms p50=${h.percentile(50)/1e6}ms p99=${h.percentile(99)/1e6}ms max=${h.max/1e6}ms`);
  h.reset();
}, 5000);

// 方法 2: 简单的事件循环延迟检测
let lastCheck = Date.now();
setInterval(() => {
  const now = Date.now();
  const delay = now - lastCheck - 1000;  // 预期 1000ms
  if (delay > 50) console.warn(`Event loop delay: ${delay}ms`);
  lastCheck = now;
}, 1000);
```

### 避免阻塞事件循环

```javascript
// ❌ 同步 JSON 解析大文件
const data = JSON.parse(fs.readFileSync('huge.json'));

// ✅ 流式解析
const JSONStream = require('JSONStream');
fs.createReadStream('huge.json')
  .pipe(JSONStream.parse('*'))
  .on('data', item => process(item));

// ❌ CPU 密集型计算在主线程
function fibonacci(n) { /* ... */ }

// ✅ 移到 Worker Thread
const { Worker } = require('worker_threads');
const worker = new Worker('./fib-worker.js', { workerData: { n: 45 } });
worker.on('message', result => console.log(result));

// ❌ 大数组同步排序
bigArray.sort((a, b) => a - b);

// ✅ 分批处理（避免长时间占用事件循环）
async function sortInChunks(arr, chunkSize = 10000) {
  for (let i = 0; i < arr.length; i += chunkSize) {
    arr.slice(i, i + chunkSize).sort((a, b) => a - b);
    await new Promise(resolve => setImmediate(resolve));  // 让出事件循环
  }
}
```

---

## 6. 优化模式

### 1. 不阻塞事件循环

```javascript
// 差：同步 I/O 阻塞
const data = fs.readFileSync('large.json');

// 好：异步
const data = await fs.promises.readFile('large.json');
```

### 2. 流式处理大文件

```javascript
// 好：恒定内存
const stream = fs.createReadStream('huge.csv');
stream.pipe(transform).pipe(output);

// 差：全部载入内存
const data = fs.readFileSync('huge.csv');
```

### 3. Worker Threads 处理 CPU 密集

```javascript
const { Worker, isMainThread, parentPort } = require('worker_threads');

if (isMainThread) {
    const worker = new Worker(__filename, { workerData: input });
    worker.on('message', result => console.log(result));
} else {
    const result = heavyComputation(workerData);
    parentPort.postMessage(result);
}
```

### 4. 连接池

```javascript
// MySQL
const pool = mysql.createPool({
    connectionLimit: 10,
    host: 'localhost',
    user: 'root',
    database: 'mydb'
});

// PostgreSQL (pg)
const pool = new Pool({ max: 20 });
```

### 5. JSON 序列化优化

```javascript
// 大对象用 fast-json-stringify（快 2-5x）
const fastJson = require('fast-json-stringify');
const stringify = fastJson({
    type: 'object',
    properties: {
        name: { type: 'string' },
        age: { type: 'integer' }
    }
});
const json = stringify({ name: 'test', age: 30 });
```

### 6. 缓存

```javascript
// 简单内存缓存
const NodeCache = require('node-cache');
const cache = new NodeCache({ stdTTL: 300 });

// Redis 缓存
const Redis = require('ioredis');
const redis = new Redis();
```

### 7. 集群模式

```javascript
const cluster = require('cluster');
const numCPUs = require('os').cpus().length;

if (cluster.isPrimary) {
    for (let i = 0; i < numCPUs; i++) {
        cluster.fork();
    }
} else {
    // 工作进程
    require('./app');
}
```

---

## 7. HTTP/网络优化

### HTTP Keep-Alive

```javascript
const http = require('http');
const agent = new http.Agent({
  keepAlive: true,
  keepAliveMsecs: 30000,
  maxSockets: 100,
  maxFreeSockets: 10
});

// 使用 undici（比 http 模块快 2-3x）
const { request } = require('undici');
const { statusCode, body } = await request('http://api.example.com/data');
```

### HTTP/2 服务器

```javascript
const http2 = require('http2');
const server = http2.createSecureServer({
  key: fs.readFileSync('key.pem'),
  cert: fs.readFileSync('cert.pem')
});
server.on('stream', (stream, headers) => {
  stream.respond({ ':status': 200 });
  stream.end('Hello HTTP/2');
});
```

### 响应压缩

```javascript
// Express
const compression = require('compression');
app.use(compression({ threshold: 1024 }));  // > 1KB 才压缩

// Fastify（推荐，比 Express 快 2-3x）
const fastify = require('fastify')({ logger: true });
await fastify.register(require('@fastify/compress'));
```

---

## 8. APM 与监控

### Prometheus + Grafana

```javascript
// prom-client（Node.js Prometheus 客户端）
const client = require('prom-client');

// 收集默认指标（GC、事件循环、内存等）
client.collectDefaultMetrics({ timeout: 5000 });

// 自定义指标
const httpDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration',
  labelNames: ['method', 'route', 'status'],
  buckets: [0.01, 0.05, 0.1, 0.5, 1, 5]
});

app.use((req, res, next) => {
  const end = httpDuration.startTimer();
  res.on('finish', () => {
    end({ method: req.method, route: req.route?.path, status: res.statusCode });
  });
  next();
});

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});
```

### PM2 生产部署

```bash
# 集群模式启动（自动利用所有 CPU）
pm2 start app.js -i max --name myapp

# 监控面板
pm2 monit

# 查看日志
pm2 logs myapp --lines 100

# 内存限制自动重启
pm2 start app.js --max-memory-restart 1G

# 生态系统配置文件 ecosystem.config.js
# module.exports = {
#   apps: [{
#     name: 'myapp',
#     script: 'app.js',
#     instances: 'max',
#     exec_mode: 'cluster',
#     max_memory_restart: '1G',
#     env: { NODE_ENV: 'production' }
#   }]
# };
```

---

## 9. 常见问题速查

| 问题 | 诊断 | 解决 |
|------|------|------|
| 事件循环阻塞 | `clinic doctor` | 异步化或移到 Worker |
| 内存泄漏 | `clinic heapprofiler` / heapdump 对比 | 检查闭包、事件监听器、全局缓存、定时器 |
| CPU 热点 | `clinic flame` / `0x` | 优化算法或移到 Worker Thread |
| 高 GC 暂停 | `--trace-gc` | 减少短生命周期对象分配、对象池、预分配 |
| OOM Crash | `--max-old-space-size` | 增大堆限制、排查泄漏、流式处理 |
| 连接耗尽 | `ss -ant` + `wc -l` | 连接池、Keep-Alive、限制并发 |
| 启动慢 | `node --trace-warnings` | 延迟加载模块、减少同步 require |
| HTTP 吞吐低 | `autocannon` | 换 Fastify、启用 cluster、HTTP/2 |

### 性能参考基准

| 场景 | 框架 | 典型 QPS (单核) |
|------|------|:-:|
| Hello World | Express | ~15,000 |
| Hello World | Fastify | ~45,000 |
| Hello World | uWebSockets.js | ~100,000+ |
| JSON 序列化 | 原生 JSON.stringify | ~2M ops/s |
| JSON 序列化 | fast-json-stringify | ~8M ops/s |
