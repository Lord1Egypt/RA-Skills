# Configuration Tuning Examples

## Example 1: Maximum Compression for Disk-Space-Constrained Cluster

**Scenario:** Cluster has limited disk space and user wants maximum compression to reduce storage usage. CPU is sufficient.

**Current Settings:**

| Setting | Current Value |
|---------|--------------|
| ts.compress.stage | 3 |
| ts.compress.algorithm | lz4 |
| ts.compress.level | medium |

**Issue:** lz4 with medium level provides moderate compression (2x-3x). Disk space is running low and higher compression is needed.

**Recommended Changes:**

| Setting | Recommended Value | Reason |
|---------|-------------------|--------|
| ts.compress.algorithm | zstd | Best compression ratio (2.5x-5x+) with reasonable speed |
| ts.compress.level | high | Maximum compression ratio (zstd-9); CPU is sufficient |

**SQL to Apply:**
```sql
SET CLUSTER SETTING ts.compress.algorithm = 'zstd';
SET CLUSTER SETTING ts.compress.level = 'high';
```

**Expected Improvement:** Disk space usage reduced by approximately 30-50% compared to lz4/medium. Write throughput may decrease by 40-60% under maximum compression.

**Validation:**
```sql
SHOW CLUSTER SETTING ts.compress.algorithm;
SHOW CLUSTER SETTING ts.compress.level;
```

---

## Example 2: CPU-Optimized Compression for Performance-Critical Workload

**Scenario:** CPU usage is high due to compression overhead. User prioritizes query and write performance over disk space savings. Disk space is sufficient.

**Current Settings:**

| Setting | Current Value |
|---------|--------------|
| ts.compress.stage | 3 |
| ts.compress.algorithm | zstd |
| ts.compress.level | high |

**Issue:** zstd with high level consumes significant CPU, causing performance bottlenecks.

**Recommended Changes:**

| Setting | Recommended Value | Reason |
|---------|-------------------|--------|
| ts.compress.algorithm | lz4 | Fast compression/decompression, low CPU overhead |
| ts.compress.level | any | No practical difference for lz4 |
| ts.compress.stage | 1 | Encoding only; remove general compression to reduce CPU overhead by 50%+ |

**SQL to Apply:**
```sql
SET CLUSTER SETTING ts.compress.algorithm = 'lz4';
SET CLUSTER SETTING ts.compress.stage = '1';
```

**Expected Improvement:** CPU overhead from compression reduced by 50%+. Disk space usage will increase since general compression is disabled. Encoding still provides some space savings with minimal CPU cost.

**Validation:**
```sql
SHOW CLUSTER SETTING ts.compress.algorithm;
SHOW CLUSTER SETTING ts.compress.stage;
```

---

## Example 3: Rows Per Block Tuning for High-Throughput Write

**Scenario:** High-throughput write workload with bulk imports. User wants to reduce flush frequency and improve compression ratio. Memory is sufficient.

**Current Settings:**

| Setting | Current Value |
|---------|--------------|
| ts.rows_per_block.min_limit | 512 |
| ts.rows_per_block.max_limit | 4096 |

**Issue:** Default max_limit causes frequent flushing under high write volume, reducing compression ratio and throughput.

**Recommended Changes:**

| Setting | Recommended Value | Reason |
|---------|-------------------|--------|
| ts.rows_per_block.max_limit | 8192 | Larger blocks reduce flush frequency, improve compression ratio for sequential write patterns |

**SQL to Apply:**
```sql
SET CLUSTER SETTING ts.rows_per_block.max_limit = 8192;
```

**Expected Improvement:** Reduced flush frequency and improved compression ratio. Block builder will pre-allocate larger bitmap/buffer, increasing memory pressure.

**Validation:**
```sql
SHOW CLUSTER SETTING ts.rows_per_block.max_limit;
```

---

## Example 4: Write Performance Optimization on HDD

**Scenario:** Write performance is slow on HDD storage. User wants to improve write throughput.

**Current Settings:**

| Setting | Current Value |
|---------|--------------|
| ts.compress.last_segment.enabled | false |

**Issue:** On HDD, not compressing last segments causes more IO during compaction rewrites, slowing write performance.

**Recommended Changes:**

| Setting | Recommended Value | Reason |
|---------|-------------------|--------|
| ts.compress.last_segment.enabled | true | Compressed last segments reduce IO on HDD, improving write performance despite slightly higher CPU usage |

**SQL to Apply:**
```sql
SET CLUSTER SETTING ts.compress.last_segment.enabled = true;
```

**Expected Improvement:** Better write performance on HDD due to reduced IO. CPU usage will increase due to compression of last segments.

**Validation:**
```sql
SHOW CLUSTER SETTING ts.compress.last_segment.enabled;
```

---

## Example 5: Cache Tuning Under Memory Pressure

**Scenario:** Memory usage is too high. User needs to release some cache memory for other operations. Query performance can tolerate some degradation.

**Current Settings:**

| Setting | Current Value |
|---------|--------------|
| ts.block.lru_cache.max_limit | 4.0 GiB |
| ts.last_cache_size.max_limit | 1.0 GiB |

**Issue:** Block LRU cache is consuming too much memory. Need to free up memory resources.

**Recommended Changes:**

| Setting | Recommended Value | Reason |
|---------|-------------------|--------|
| ts.block.lru_cache.max_limit | 2.0 GiB | Reduce cache size to free memory; query performance may degrade slightly |
| ts.last_cache_size.max_limit | 512 MiB | Reduce last cache size; last query cache hit rate may decrease |

**SQL to Apply:**
```sql
SET CLUSTER SETTING ts.block.lru_cache.max_limit = '2.0 GiB';
SET CLUSTER SETTING ts.last_cache_size.max_limit = '512 MiB';
```

**Expected Improvement:** Approximately 2.5 GiB memory freed. Block query and last query performance may degrade due to reduced cache sizes.

**Validation:**
```sql
SHOW CLUSTER SETTING ts.block.lru_cache.max_limit;
SHOW CLUSTER SETTING ts.last_cache_size.max_limit;
```

---

## Example 6: Compaction Tuning for Segment Backlog

**Scenario:** Compaction is falling behind with significant segment backlog. CPU has idle capacity. User wants to speed up compaction.

**Current Settings:**

| Setting | Current Value |
|---------|--------------|
| ts.compact.max_limit | 10 |
| ts.reserved_last_segment.max_limit | 3 |

**Issue:** Default compaction batch size is insufficient to keep up with the write rate, causing segment backlog.

**Recommended Changes:**

| Setting | Recommended Value | Reason |
|---------|-------------------|--------|
| ts.compact.max_limit | 20 | Merge more segments per compaction run to reduce backlog |
| ts.reserved_last_segment.max_limit | 5 | Allow more segments to accumulate before compaction, reducing compaction frequency |

**SQL to Apply:**
```sql
SET CLUSTER SETTING ts.compact.max_limit = 20;
SET CLUSTER SETTING ts.reserved_last_segment.max_limit = 5;
```

**Expected Improvement:** Fewer total compaction runs, faster segment backlog clearance. Single compaction runs will take longer with higher CPU/IO peak pressure. Unmerged segments will occupy more temporary disk space.

**Validation:**
```sql
SHOW CLUSTER SETTING ts.compact.max_limit;
SHOW CLUSTER SETTING ts.reserved_last_segment.max_limit;
```