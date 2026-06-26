# L76 Core Architecture - Performance Tuning Guide

Optimize skill execution for speed, memory efficiency, and reliability.

## Performance Metrics

Target metrics for production-ready skills:

| Metric | Target | Acceptable | Action Required |
|--------|--------|------------|-----------------|
| Cold start time | <2s | <5s | >10s |
| Tool call latency | <500ms | <2s | >5s |
| Memory usage | <50MB | <200MB | >500MB |
| Success rate | >99% | >95% | <90% |
| Error recovery time | <5s | <15s | >30s |

## Profiling Tools

### Built-in Node.js Profiling

```bash
# CPU profiling
node --prof index.js
node --prof-process isolate-*.log > profile.txt

# Memory profiling
node --inspect index.js
# Connect Chrome DevTools to ws://... endpoint
# Use Memory tab for heap snapshots

# Timing individual operations
node -e "
console.time('operation');
// your code here
console.timeEnd('operation');
"
```

### Custom Timing Wrapper

```javascript
class PerformanceMonitor {
  constructor() {
    this.timings = new Map();
  }

  start(label) {
    this.timings.set(label, { start: Date.now() });
  }

  end(label) {
    const timing = this.timings.get(label);
    if (!timing) return;
    timing.duration = Date.now() - timing.start;
    console.log(`⏱️ ${label}: ${timing.duration}ms`);
    return timing.duration;
  }

  summary() {
    const total = Array.from(this.timings.values())
      .reduce((sum, t) => sum + (t.duration || 0), 0);
    console.log(`📊 Total execution: ${total}ms`);
    return { total, timings: Object.fromEntries(this.timings) };
  }
}

// Usage
const perf = new PerformanceMonitor();
perf.start('read-files');
await readFiles();
perf.end('read-files');
```

---

## Optimization Strategies

### 1. Reduce Tool Call Overhead

**Problem:** Each tool call has ~100-300ms overhead.

**Solutions:**

#### Batch Related Operations

```javascript
// ❌ Slow - 10 separate read calls (10 × 300ms = 3s overhead)
for (let i = 0; i < 10; i++) {
  const content = await read({ path: `file${i}.txt` });
}

// ✅ Fast - Single exec to read all files
const result = await exec({ 
  command: 'cat file*.txt',
  timeout: 30000
});
```

#### Combine Read + Process

```javascript
// ❌ Two tool calls
const content = await read({ path: 'data.json' });
const parsed = JSON.parse(content);

// ✅ One tool call with inline processing
const result = await exec({
  command: 'node -e "console.log(JSON.parse(require(\'fs\').readFileSync(\'data.json\')))"'
});
```

#### Use Efficient Tool Selection

| Task | Preferred Tool | Why |
|------|---------------|-----|
| Read single file | `read` | Simple, reliable |
| Read multiple files | `exec` (cat) | Single call, faster |
| Search file content | `exec` (grep/rg) | Optimized for search |
| Fetch web page | `web_fetch` | Lighter than `browser` |
| Complex web interaction | `browser` | Full automation |

---

### 2. Memory Management

**Problem:** Large files or datasets cause memory bloat.

**Solutions:**

#### Stream Large Files

```javascript
// ❌ Loads entire file into memory
const content = await read({ path: 'huge-file.log' });

// ✅ Process in chunks
const CHUNK_SIZE = 1000; // lines
let offset = 0;

while (true) {
  const chunk = await read({ 
    path: 'huge-file.log',
    offset: offset,
    limit: CHUNK_SIZE
  });
  
  if (!chunk || chunk.length === 0) break;
  
  processChunk(chunk);
  offset += CHUNK_SIZE;
}
```

#### Limit Array Growth

```javascript
// ❌ Unbounded array growth
const errors = [];
errors.push(error); // Grows forever

// ✅ Fixed-size buffer
const MAX_ERRORS = 100;
if (errors.length >= MAX_ERRORS) {
  errors.shift(); // Remove oldest
}
errors.push(error);

// Or use state trimming
state.errors = state.errors.slice(-MAX_ERRORS);
```

#### Clear References

```javascript
async function processLargeDataset(items) {
  const results = [];
  
  for (const item of items) {
    const result = await processItem(item);
    results.push(result);
    
    // Clear reference to allow GC
    item.largeData = null;
  }
  
  // Force GC if needed (Node.js with --expose-gc)
  if (global.gc) {
    global.gc();
  }
  
  return results;
}
```

---

### 3. Concurrency Control

**Problem:** Too many parallel tool calls overwhelm the system.

**Solutions:**

#### Implement Concurrency Limits

```javascript
// ❌ No limit - all calls at once
const results = await Promise.all(
  files.map(f => read({ path: f }))
);

// ✅ Limited concurrency
async function mapWithConcurrency(items, fn, limit = 5) {
  const results = [];
  const executing = [];
  
  for (const item of items) {
    const promise = fn(item).then(result => {
      results.push(result);
      executing.splice(executing.indexOf(promise), 1);
      return result;
    });
    
    executing.push(promise);
    
    if (executing.length >= limit) {
      await Promise.race(executing);
    }
  }
  
  await Promise.all(executing);
  return results;
}

// Usage
const results = await mapWithConcurrency(files, f => read({ path: f }), 5);
```

#### Sequential for Dependent Operations

```javascript
// ✅ Sequential when order matters
for (const migration of migrations) {
  await applyMigration(migration);
  // Wait for each to complete before next
}
```

---

### 4. Caching Strategies

**Problem:** Repeated expensive operations.

**Solutions:**

#### In-Memory Cache (Single Run)

```javascript
class Cache {
  constructor() {
    this.cache = new Map();
  }

  async get(key, fn) {
    if (this.cache.has(key)) {
      return this.cache.get(key);
    }
    
    const value = await fn();
    this.cache.set(key, value);
    return value;
  }
}

// Usage
const cache = new Cache();
const config = await cache.get('config', () => read({ path: 'config.json' }));
```

#### Persistent Cache (Cross-Run)

```javascript
class PersistentCache {
  constructor(cacheFile) {
    this.cacheFile = cacheFile;
    this.cache = this.load();
  }

  load() {
    try {
      if (fs.existsSync(this.cacheFile)) {
        return JSON.parse(fs.readFileSync(this.cacheFile));
      }
    } catch (e) {
      console.warn('Cache load failed:', e.message);
    }
    return {};
  }

  save() {
    try {
      fs.writeFileSync(this.cacheFile, JSON.stringify(this.cache));
    } catch (e) {
      console.warn('Cache save failed:', e.message);
    }
  }

  async get(key, fn, ttlMs = 3600000) {
    const entry = this.cache[key];
    const now = Date.now();
    
    if (entry && (now - entry.timestamp) < ttlMs) {
      return entry.value;
    }
    
    const value = await fn();
    this.cache[key] = { value, timestamp: now };
    this.save();
    return value;
  }
}
```

---

### 5. Timeout Management

**Problem:** Tool calls hang indefinitely.

**Solutions:**

#### Set Explicit Timeouts

```javascript
// ❌ No timeout - can hang forever
await exec({ command: 'slow-command' });

// ✅ Explicit timeout
await exec({ 
  command: 'slow-command',
  timeout: 30 // seconds
});

// ✅ Timeout with retry
async function execWithRetry(command, maxRetries = 3, timeout = 30) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await exec({ command, timeout });
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      // Exponential backoff
      await sleep(1000 * Math.pow(2, i));
    }
  }
}
```

#### Timeout Wrapper for Any Operation

```javascript
function withTimeout(promise, ms, label = 'operation') {
  const timeout = new Promise((_, reject) => {
    setTimeout(() => reject(new Error(`${label} timed out after ${ms}ms`)), ms);
  });
  
  return Promise.race([promise, timeout]);
}

// Usage
const result = await withTimeout(
  read({ path: 'file.txt' }),
  10000,
  'file-read'
);
```

---

### 6. Error Recovery Optimization

**Problem:** Error handling slows down success path.

**Solutions:**

#### Fast-Fail for Non-Recoverable Errors

```javascript
// ❌ Try-catch around everything
try {
  await read({ path: 'required.json' });
} catch (e) {
  // Log, retry, fallback...
}

// ✅ Validate first, fail fast
const exists = await exec({ command: 'test -f required.json' });
if (exists.exitCode !== 0) {
  return { status: 'error', error: 'Required file missing' };
}
// Now proceed without try-catch
```

#### Circuit Breaker Pattern

```javascript
class CircuitBreaker {
  constructor(threshold = 5, timeout = 60000) {
    this.failures = 0;
    this.threshold = threshold;
    this.timeout = timeout;
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
    this.nextAttempt = 0;
  }

  async execute(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() < this.nextAttempt) {
        throw new Error('Circuit breaker OPEN');
      }
      this.state = 'HALF_OPEN';
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failures = 0;
    this.state = 'CLOSED';
  }

  onFailure() {
    this.failures++;
    if (this.failures >= this.threshold) {
      this.state = 'OPEN';
      this.nextAttempt = Date.now() + this.timeout;
    }
  }
}
```

---

## Performance Checklist

Before deploying a skill:

- [ ] **Cold start <5s** - Measure time from trigger to first output
- [ ] **Tool calls minimized** - Batch where possible
- [ ] **Memory <200MB** - Profile with Node.js inspector
- [ ] **Timeouts set** - All external calls have explicit timeouts
- [ ] **Errors handled** - Recovery paths tested
- [ ] **Cache implemented** - Expensive operations cached
- [ ] **Concurrency limited** - No unbounded parallelism
- [ ] **State trimmed** - Arrays/files don't grow unbounded

---

## Benchmarking Template

```javascript
const { PerformanceMonitor } = require('./perf-monitor');

async function benchmark() {
  const perf = new PerformanceMonitor();
  const iterations = 10;
  const results = [];

  console.log(`🏃 Running ${iterations} iterations...`);

  for (let i = 0; i < iterations; i++) {
    perf.start(`run-${i}`);
    
    // Your skill logic here
    await runSkill();
    
    const duration = perf.end(`run-${i}`);
    results.push(duration);
  }

  // Statistics
  const avg = results.reduce((a, b) => a + b, 0) / results.length;
  const min = Math.min(...results);
  const max = Math.max(...results);
  const p95 = results.sort((a, b) => a - b)[Math.floor(results.length * 0.95)];

  console.log('');
  console.log('📊 Performance Summary:');
  console.log(`  Average: ${avg.toFixed(0)}ms`);
  console.log(`  Min: ${min}ms`);
  console.log(`  Max: ${max}ms`);
  console.log(`  P95: ${p95}ms`);

  return { avg, min, max, p95, results };
}

// Run benchmark
if (require.main === module) {
  benchmark();
}
```

---

## Common Performance Anti-Patterns

| Anti-Pattern | Impact | Fix |
|--------------|--------|-----|
| Polling in tight loop | CPU spike, rate limits | Add delay or use webhooks |
| Reading entire large file | Memory bloat | Stream in chunks |
| No timeout on network calls | Hangs forever | Always set timeout |
| Unbounded array growth | Memory leak | Trim or use fixed buffer |
| Sequential when parallel OK | Slow execution | Use Promise.all with limit |
| Parallel when sequential needed | Race conditions | Use for-loop |
| No caching of repeated reads | Slow, wasteful | Implement cache |
| Logging in hot path | I/O overhead | Log asynchronously or sample |

---

**Last Updated:** 2026-03-22  
**Version:** 1.0.0  
**Maintainer:** openclaw
