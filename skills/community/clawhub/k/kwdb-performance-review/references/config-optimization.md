# Storage Configuration Optimization

## Activation Rules

- Only consider configuration optimization when the user explicitly mentions "config optimization" / "parameter tuning" / "配置优化" / "参数调优", or SQL query optimization steps are exhausted and performance issues persist
- User must confirm current database memory and disk space usage
- Only provide configuration suggestions; execution requires user confirmation
- Always prompt relevant risks when adjusting parameters

## How to Query Config Values

- With MCP: query individual settings via `mcp__kwdb__read-query("SHOW CLUSTER SETTING ts.xxx")`
- Without MCP: ask user to run `SHOW CLUSTER SETTING ts.xxx;`
- NEVER use `SHOW CLUSTER SETTINGS` to query all configuration info

## Per-Parameter Trigger Conditions

| Parameter | Config Group | Trigger Condition |
|-----------|-------------|-------------------|
| ts.compress.stage | Compression Group | User wants compression optimization or smaller disk space usage |
| ts.compress.algorithm | Compression Group | User wants compression optimization or smaller disk space usage |
| ts.compress.level | Compression Group | User wants compression optimization or smaller disk space usage |
| ts.rows_per_block.min_limit | Rows Per Block Group | User reports excessive small blocks from flushing, long write visibility delay, or high per-device data volume with low compression ratio |
| ts.rows_per_block.max_limit | Rows Per Block Group | User reports excessive small blocks from flushing, long write visibility delay, or high per-device data volume with low compression ratio |
| ts.compress.last_segment.enabled | Independent | User wants compression optimization or smaller disk space usage, or needs to optimize write performance |
| ts.block.lru_cache.max_limit | Independent | User wants to optimize overall query performance, or memory usage is too high |
| ts.last_cache_size.max_limit | Independent | User wants to optimize last-related SQL query performance, or memory usage is too high |
| ts.mem_segment_size.max_limit | Independent | Write performance optimization (after ts.compress.last_segment.enabled reviewed), or memory usage is too high (after ts.block.lru_cache.max_limit and ts.last_cache_size.max_limit reviewed) |
| ts.reserved_last_segment.max_limit | Independent | Frequent compaction triggers or disk space is tight |
| ts.compact.max_limit | Independent | User reports compaction backlog with significant CPU idle, or CPU usage is too high |
| ts.auto_vacuum.enabled | Independent | User wants to clean up data |
| ts.block_filter.sampling_ratio | Independent | User reports poor query performance with range conditions or null checks, suspects inefficient filter pushdown |

## Group 1: Compression Group

### ts.compress.stage

- Time-series database compression level
- Range: 0-3
- Default: 3
- Increase Impact: Encoding + compression provides optimal compression ratio, but highest CPU overhead; write throughput may decrease under high compression settings
- Decrease Impact: Disk space usage increases

| Value | Use Case | Risk |
|-------|----------|------|
| 0 | Unlimited disk space; no compression CPU overhead | Large disk space usage |
| 1 | Performance priority; encoding only; minimal CPU overhead | No general compression, space savings inferior to stage 2/3 |
| 2 | Compression only, no encoding | Less space-efficient than stage=3 (lacks encoding preprocessing, lower general compression efficiency) |
| 3 | Best compression ratio (default); encoding + compression provides optimal results | No risk |

**Pre-condition**: Confirm disk space status

**Dependencies**: ts.compress.algorithm, ts.compress.level (these three parameters have dependencies and must be reviewed together)

### ts.compress.algorithm

- General compression algorithm for time-series data
- Value: disabled, snappy, lz4, zlib, zstd
- Default: lz4
- Increase Impact (choosing higher compression ratio algorithm): Increased CPU usage, decreased disk space usage
- Decrease Impact (choosing lower compression ratio algorithm): Decreased CPU usage, increased disk space usage

| Value | Use Case | Risk |
|-------|----------|------|
| disabled | Unlimited disk space | No compression, highest disk space usage |
| snappy | Fast compression/decompression, low CPU and memory overhead; compression ratio 1.5x-2x; suitable when CPU is constrained | Lowest compression ratio |
| lz4 | Fast compression/decompression, low CPU and memory overhead, compression ratio 2x-3x | Lower compression ratio than zstd/zlib |
| zlib | General-purpose compression algorithm, good compatibility, compression ratio 2.5x-4x | Compression ratio and speed lower than zstd |
| zstd | General-purpose compression algorithm, best balance of speed and compression ratio, compression ratio 2.5x-5x+ | Higher CPU and memory usage at high compression levels |

**Pre-condition**: Confirm CPU and disk space status

**Dependencies**: ts.compress.stage, ts.compress.level (these three parameters have dependencies and must be reviewed together)

**Special Cases**: The level parameter has no practical effect for lz4/snappy

### ts.compress.level

- Compression level for the general time-series data compression algorithm
- Value: low, medium, high
- Default: medium
- Increase Impact: Higher compression ratio, but significantly increased compression/decompression CPU usage
- Decrease Impact: Lower CPU usage, but lower compression ratio

| Value | Use Case | Risk |
|-------|----------|------|
| low | Performance priority; minimal CPU overhead; no practical difference for lz4/snappy | Lowest compression ratio; zstd (zstd-1) / zlib (zlib-1) have limited compression |
| medium | General use (default); zstd (zstd-3) / zlib (zlib-6) | |
| high | Disk space priority, CPU sufficient; zstd (zstd-9) / zlib (zlib-9) | Higher compression/decompression CPU usage |

**Pre-condition**: Confirm CPU and disk space status

**Dependencies**: ts.compress.stage, ts.compress.algorithm (these three parameters have dependencies and must be reviewed together)

**Special Cases**: The level parameter has no practical effect for lz4/snappy; level mapping: zstd: low=1, medium=3, high=9; zlib: low=1, medium=6, high=9

### Compression Group Decision

- Scenario 1: Performance priority, disk space sufficient → algorithm=snappy/lz4, level=any (no difference for lz4/snappy), stage=1 (encoding only); extreme performance use stage=0
- Scenario 2: Disk space priority, CPU sufficient → algorithm=zstd, level=high, stage=3 (encoding+compression); maximum compression may reduce write throughput by 40-60%
- Scenario 3: CPU usage too high → algorithm=lz4, level=any, stage=1 (encoding only); removing general compression reduces CPU overhead by 50%+; if still too high, try stage=0
- Core principle: Encoding is a "free lunch" leveraging time-series data structure features with minimal CPU overhead but significant compression effect. Almost all scenarios recommend keeping it (stage ≥ 1). The real trade-off is which algorithm and level to use for the general compression stage.

**Dependencies**: ts.compress.stage / ts.compress.algorithm / ts.compress.level have dependencies and must be reviewed together

## Group 2: Rows Per Block Group

### ts.rows_per_block.min_limit

- Minimum number of rows a block can hold in an entity segment
- Range: Positive integer
- Default: 512
- Increase Impact: Fewer blocks, lower metadata overhead, but longer compaction time
- Decrease Impact: More small blocks, increased metadata overhead and compaction pressure

| Value | Use Case | Risk |
|-------|----------|------|
| 128 | Very small data volume per partition per device (<128 rows), want to improve compression ratio | Easier to meet flush threshold, producing more small blocks → increased metadata overhead and compaction pressure |
| 256 | Small data volume per partition per device (128-256 rows) | More small blocks, increased metadata overhead and compaction pressure |
| 512 | Default | |
| 1024+ | Low-latency write, frequent small batch writes | Need to accumulate more rows before flushing, write latency may increase |

**Pre-condition**: Confirm data volume per partition per device

**Dependencies**: ts.rows_per_block.max_limit (these two parameters have dependencies and must be reviewed together)

### ts.rows_per_block.max_limit

- Maximum number of rows a block can hold in an entity segment
- Range: Positive integer
- Default: 4096
- Increase Impact: Higher compression ratio, saves storage space
- Decrease Impact: Less data scanned per query, faster query response

| Value | Use Case | Risk |
|-------|----------|------|
| 2048 | Memory constrained; point queries dominant | More frequent flushing, lower throughput; lower compression ratio |
| 4096 | Default | |
| 8192 | High-throughput write, bulk import, sequential scan/analysis dominant | Block builder pre-allocates larger bitmap/buffer, increased memory pressure |
| 16384 | Extremely high throughput write, disk space priority | Maximum memory pre-allocation overhead |

**Pre-condition**: Confirm data volume per partition per device and memory status

**Dependencies**: ts.rows_per_block.min_limit (these two parameters have dependencies and must be reviewed together)

**Special Cases**: Bitmap and offset buffer are pre-allocated based on max_rows_per_block; even if a block only writes a few hundred rows, memory is allocated at the upper limit. Vacuum operations are not subject to minimum row count restrictions, ensuring garbage data can be cleaned up promptly.

### Rows Per Block Group Decision

- Scenario 1: High-throughput write, bulk import → increase max (8192-16384), reduce flush frequency, improve compression ratio
- Scenario 2: Memory constrained → decrease max (2048), reduce pre-allocation overhead
- Scenario 3: Point queries dominant → decrease max moderately, lighter single-block loading
- Scenario 4: Sequential scan/analysis dominant → increase max, reduce metadata overhead, improve compression ratio and scan efficiency
- Scenario 5: Low-latency write, frequent small batch → increase min moderately (1024+), avoid frequent small block flushes

**Dependencies**: ts.rows_per_block.min_limit / ts.rows_per_block.max_limit have dependencies and must be reviewed together

## Independent Parameters

### ts.compress.last_segment.enabled

- Whether to compress last segments
- Default: false
- Controls whether last segments are compressed. Last segments are frequently rewritten during compaction; not compressing reduces CPU overhead during compaction.

**Special Cases**:
- SSD: false (default) — better write performance, but higher last segment file space usage
- HDD: true — better write performance (less IO), but higher CPU usage
- Enable (true) when disk space is tight; disable (false) when disk space is sufficient

**Risk**: Setting to true increases CPU usage

**Important**: When write performance is slow, consider this parameter first, rather than ts.mem_segment_size.max_limit

### ts.block.lru_cache.max_limit

- Maximum memory space for block LRU cache
- Range: 0 = cache disabled; otherwise memory size string (e.g., "2.0 GiB")
- Default: 1.0 GiB
- Recommended Limit: 10 GiB
- Increase Impact: Better query performance, increased memory usage; user must confirm sufficient free memory
- Decrease Impact: Lower query performance, reduced memory usage; database read/write performance may degrade

| Value | Use Case | Risk |
|-------|----------|------|
| 0 | Extremely tight memory, need to release cache | Database read/write performance may degrade |
| 1.0 GiB | Default | |
| 2.0-4.0 GiB | Query performance needs improvement, sufficient free memory | Increased memory usage |
| 4.0-10.0 GiB | Query-intensive workload, very abundant memory | Significantly increased memory usage |

**Pre-condition**: Confirm available free memory

### ts.last_cache_size.max_limit

- Maximum memory space for last cache
- Range: 0 = cache disabled; maximum 1.0 GiB
- Default: 1.0 GiB
- Recommended Limit: 1 GiB
- Increase Impact: Better last query performance, increased memory usage; user must confirm sufficient free memory
- Decrease Impact: Lower last query performance, reduced memory usage

| Value | Use Case | Risk |
|-------|----------|------|
| 0 | Extremely tight memory, need to release cache | Last query performance degrades |
| 512 MiB | Tight memory, low last query frequency | Reduced last query cache hit rate |
| 1.0 GiB | Default | |

**Pre-condition**: Confirm available free memory

### ts.mem_segment_size.max_limit

- Maximum memory space for mem segments retained in vgroups
- Range: Memory size string (e.g., "256 MiB")
- Default: 128 MiB
- Recommended Limit: 1 GiB
- Increase Impact: Better write performance, increased memory usage, reduced data persistence frequency; user must confirm sufficient free memory; modifying this parameter is not recommended
- Decrease Impact: Lower write performance, reduced memory usage, faster data persistence frequency; modifying this parameter is not recommended

| Value | Use Case | Risk |
|-------|----------|------|
| 64 MiB | Low-frequency write scenario, tight memory | Lower write performance; modifying this parameter is not recommended |
| 128 MiB | Default | |
| 256-512 MiB | Write performance needs improvement, sufficient free memory | Increased memory usage; modifying this parameter is not recommended |

**Pre-condition**: Confirm available free memory; explicitly inform user that modifying this parameter is not recommended

**Important**: Modifying this parameter is not recommended. For slow write performance, consider the ts.compress.last_segment.enabled configuration parameter first.

### ts.reserved_last_segment.max_limit

- Maximum number of last segments retained per partition
- Range: Positive integer
- Default: 3
- Increase Impact: More last segments accumulate, increased temporary disk space usage
- Decrease Impact: Faster merging, quicker disk space reclamation, but higher CPU usage

| Value | Use Case | Risk |
|-------|----------|------|
| 2 | Point queries / low-latency reads; disk space tight | More frequent compaction triggers, competing with writes for resources, lower throughput |
| 3 | Default | |
| 5 | Bulk write/import; analysis queries / sequential scans | Unmerged segment accumulation, increased read amplification; increased temporary disk space usage |

**Pre-condition**: Confirm whether disk space is sufficient, confirm write workload type

### ts.compact.max_limit

- Maximum number of last segments merged in a single compaction
- Range: Positive integer
- Default: 10
- Increase Impact: Higher single-compaction efficiency, fewer compaction runs, but higher CPU usage
- Decrease Impact: Less work per compaction, lower CPU and I/O peak pressure, but more total compaction runs

| Value | Use Case | Risk |
|-------|----------|------|
| 3-5 | Low-latency requirements, concurrent read/write; resource constrained (CPU/memory tight) | More total compaction runs |
| 10 | General mixed workload (default) | |
| 20 | High write rate, severe segment backlog | Longer single compaction time, higher CPU and I/O peak pressure |

**Pre-condition**: Confirm compaction backlog status and CPU idle level

### ts.auto_vacuum.enabled

- Whether automatic reorganization tasks are enabled
- Default: true
- If automatic reorganization/cleanup to free disk space is not needed, this can be disabled

### ts.block_filter.sampling_ratio

- Filter pushdown sampling ratio
- Range: (0.0, 1.0]
- Default: 0.2
- Increase Impact: More accurate sampling, reduces risk of misjudging and abandoning full filtering, avoids unnecessary block scans; but increased CPU overhead
- Decrease Impact: Lower CPU overhead during sampling, but prone to misjudgment and abandoning full filtering, causing blocks that could be skipped to still be scanned, slowing queries (does not affect result correctness)

| Value | Use Case | Risk |
|-------|----------|------|
| 0.05~0.1 | Queries rarely filter blocks (full table scan dominant) | Insufficient sampling representativeness, prone to misjudgment and abandoning full filtering, query performance degrades to unfiltered scan |
| 0.2 | General use (default), balance point | |
| 1.0 | Filter conditions hit many blocks, need precise prediction | Increased sampling CPU overhead; setting to 1.0 loses the meaning of sampling |

**Pre-condition**: Confirm CPU idle level

## Decision Tree

1. **Compression optimization / disk space reduction needed** → Compression Group
   - Performance priority, disk space sufficient → algorithm=snappy/lz4, level=any (no difference for lz4/snappy), stage=1 (encoding only); extreme performance use stage=0
   - Disk space priority, CPU sufficient → algorithm=zstd, level=high, stage=3 (encoding+compression); maximum compression may reduce write throughput by 40-60%
   - CPU usage too high → algorithm=lz4, level=any, stage=1 (encoding only); removing general compression reduces CPU overhead by 50%+; if still too high, try stage=0
   - Core principle: Encoding is a "free lunch" (stage ≥ 1 recommended). The real trade-off is general compression algorithm and level choice.

2. **Excessive small blocks / write visibility delay / low compression ratio** → Rows Per Block Group
   - High-throughput write, bulk import → increase max (8192-16384), reduce flush frequency, improve compression ratio
   - Memory constrained → decrease max (2048), reduce pre-allocation overhead
   - Point queries dominant → decrease max moderately, lighter single-block loading
   - Sequential scan/analysis dominant → increase max, reduce metadata overhead, improve compression ratio and scan efficiency
   - Low-latency write, frequent small batch → increase min (1024+), avoid frequent small block flushes

3. **Write performance optimization** → ts.compress.last_segment.enabled
   - SSD: false (default) — better write performance
   - HDD: true — less IO, better write performance
   - Consider this parameter first before ts.mem_segment_size.max_limit

4. **Overall query performance / high memory usage** → ts.block.lru_cache.max_limit
   - Memory tight → decrease (risk: database read/write performance may degrade)
   - Query performance needs improvement, memory sufficient → increase

5. **Last query performance / high memory usage** → ts.last_cache_size.max_limit
   - Memory tight → decrease (risk: last query performance degrades)
   - Note: Maximum value equals default (1.0 GiB), only decrease direction applies

6. **Write performance (after last_segment.enabled reviewed) / high memory usage (after caches reviewed)** → ts.mem_segment_size.max_limit
   - Modifying this parameter is not recommended; consider ts.compress.last_segment.enabled first for write performance issues
   - Memory tight → decrease (risk: write performance degrades)
   - Memory sufficient, write performance needs improvement → increase (not recommended)

7. **Frequent compaction / disk space tight** → ts.reserved_last_segment.max_limit
   - Disk space tight or point queries → decrease (risk: more frequent compaction, competing with writes)
   - Bulk write/import or analysis queries → increase (risk: read amplification, more temp disk space)

8. **Compaction backlog / high CPU usage** → ts.compact.max_limit
   - Compaction backlog, CPU idle → increase (risk: longer single compact, higher CPU/IO peak)
   - Low latency, concurrent read/write → decrease (risk: more total compaction runs)

9. **Data cleanup needed** → ts.auto_vacuum.enabled
   - Disable if automatic reorganization/cleanup is not needed

10. **Poor filter pushdown query performance** → ts.block_filter.sampling_ratio
    - Full table scan dominant → decrease (risk: filter pushdown may be ineffective, query degrades to unfiltered scan)
    - Filter conditions hit many blocks → increase (risk: sampling CPU overhead increases)

## Config Query Reference

| Parameter | Query SQL |
|-----------|-----------|
| ts.compress.stage | `SHOW CLUSTER SETTING ts.compress.stage;` |
| ts.compress.algorithm | `SHOW CLUSTER SETTING ts.compress.algorithm;` |
| ts.compress.level | `SHOW CLUSTER SETTING ts.compress.level;` |
| ts.rows_per_block.min_limit | `SHOW CLUSTER SETTING ts.rows_per_block.min_limit;` |
| ts.rows_per_block.max_limit | `SHOW CLUSTER SETTING ts.rows_per_block.max_limit;` |
| ts.compress.last_segment.enabled | `SHOW CLUSTER SETTING ts.compress.last_segment.enabled;` |
| ts.block.lru_cache.max_limit | `SHOW CLUSTER SETTING ts.block.lru_cache.max_limit;` |
| ts.last_cache_size.max_limit | `SHOW CLUSTER SETTING ts.last_cache_size.max_limit;` |
| ts.mem_segment_size.max_limit | `SHOW CLUSTER SETTING ts.mem_segment_size.max_limit;` |
| ts.reserved_last_segment.max_limit | `SHOW CLUSTER SETTING ts.reserved_last_segment.max_limit;` |
| ts.compact.max_limit | `SHOW CLUSTER SETTING ts.compact.max_limit;` |
| ts.auto_vacuum.enabled | `SHOW CLUSTER SETTING ts.auto_vacuum.enabled;` |
| ts.block_filter.sampling_ratio | `SHOW CLUSTER SETTING ts.block_filter.sampling_ratio;` |

## Configuration Examples

See `assets/example-configs.md` for detailed configuration tuning examples.
