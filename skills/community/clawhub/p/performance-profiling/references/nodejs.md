# Node.js 性能分析

## 内置分析

```bash
# V8 分析
node --prof app.js
node --prof-process isolate-*.log

# CPU 分析
node --cpu-prof app.js
# 生成 CPU-*.cpuprofile，Chrome DevTools 打开

# 堆快照
node --heap-prof app.js
```

## clinic.js

```bash
npm install -g clinic

# CPU 分析
clinic doctor -- node app.js

# 事件循环延迟
clinic bubbleprof -- node app.js

# 内存分析
clinic heapprofiler -- node app.js

# 火焰图
clinic flame -- node app.js
```

## 0x 火焰图

```bash
npm install -g 0x
0x app.js
```

## 代码调试

```javascript
// console.time
console.time('operation');
// ... 代码
console.timeEnd('operation');

// performance API
const { performance } = require('perf_hooks');
const start = performance.now();
// ... 代码
const end = performance.now();
console.log(`耗时: ${end - start}ms`);

// 内存使用
const used = process.memoryUsage();
console.log({
  rss: `${used.rss / 1024 / 1024} MB`,
  heapUsed: `${used.heapUsed / 1024 / 1024} MB`,
});
```
