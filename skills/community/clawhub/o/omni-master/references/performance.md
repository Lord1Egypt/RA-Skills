# Performance & Optimization Engine

Making things faster, leaner, and more efficient — code, processes, and resource usage.

---

## 1. Performance Analysis

### Profiling
```python
# Python timing
import time
start = time.perf_counter()
# ... code to measure ...
elapsed = time.perf_counter() - start
print(f"Took {elapsed:.4f}s")

# cProfile for detailed profiling
import cProfile
cProfile.run('my_function()')

# Memory usage
import tracemalloc
tracemalloc.start()
# ... code ...
current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current/1024:.1f}KB, Peak: {peak/1024:.1f}KB")
```

```bash
# Shell timing
time ./script.sh

# strace for syscall profiling
strace -c ./program
```

### Big-O Complexity
| Notation | Name | Example |
|---|---|---|
| O(1) | Constant | Hash lookup |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Simple loop |
| O(n log n) | Linearithmic | Merge sort |
| O(n²) | Quadratic | Nested loops |
| O(2ⁿ) | Exponential | Recursive fibonacci |
| O(n!) | Factorial | Permutations |

---

## 2. Code Optimization

### Python
```python
# SLOW: Repeated string concatenation
result = ""
for s in strings:
    result += s  # O(n²) total

# FAST: Join
result = "".join(strings)  # O(n)

# SLOW: List search
found = item in large_list  # O(n)

# FAST: Set lookup
found = item in large_set   # O(1)

# SLOW: Building list with append in loop
result = []
for x in data:
    result.append(f(x))

# FAST: List comprehension
result = [f(x) for x in data]

# FASTEST: Generator (lazy, memory-efficient)
result = (f(x) for x in data)
```

### JavaScript
```javascript
// SLOW: Repeated DOM queries
for (let i = 0; i < 1000; i++) {
    document.getElementById('x').style.color = 'red';
}

// FAST: Cache reference
const el = document.getElementById('x');
for (let i = 0; i < 1000; i++) {
    el.style.color = 'red';
}

// SLOW: For...of on large arrays
for (const item of hugeArray) { ... }

// FAST: Classic for loop
for (let i = 0; i < hugeArray.length; i++) { ... }
```

### Database
```sql
-- SLOW: No index
SELECT * FROM users WHERE email = 'test@example.com';

-- FAST: With index
CREATE INDEX idx_users_email ON users(email);

-- SLOW: N+1 queries
-- for each order, query user separately

-- FAST: JOIN
SELECT orders.*, users.name 
FROM orders JOIN users ON orders.user_id = users.id;
```

---

## 3. Process Optimization

### Parallelization
```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# I/O bound: use threads
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(fetch_url, urls))

# CPU bound: use processes
with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(heavy_computation, data))
```

### Caching
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(param):
    # Result cached for repeated calls
    return compute(param)
```

### Batching
```python
# SLOW: One API call per item
for item in items:
    api.send(item)  # 1000 network calls

# FAST: Batch API calls
for batch in chunks(items, 100):
    api.send_batch(batch)  # 10 network calls
```

---

## 4. Resource Optimization

### Memory
- Process data in streams/chunks, not all at once
- Use generators over lists when iterating once
- Delete large objects when done: `del big_data`
- Use appropriate data types (int32 vs int64)

### Disk
- Compress large files: gzip, lz4
- Use binary formats (Parquet, Avro) over text (CSV)
- Clean up temp files
- Log rotation

### Network
- Batch requests
- Compress payloads (gzip)
- Cache responses (ETags, TTL)
- Connection pooling
- CDN for static assets

---

## 5. Monitoring & Metrics

### Key Metrics
- **Latency**: Response time (p50, p95, p99)
- **Throughput**: Requests/operations per second
- **Error rate**: Failed operations / total
- **Resource usage**: CPU, memory, disk, network
- **Saturation**: How close to capacity

### Quick Monitoring
```bash
# System resources
top -bn1 | head -5
free -h
df -h
iostat 1 3

# Process-specific
ps aux --sort=-%mem | head -10
ps aux --sort=-%cpu | head -10
```
