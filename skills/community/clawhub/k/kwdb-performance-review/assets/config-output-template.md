## For Configuration Optimization

## Intent
[Brief description — e.g., "Review compression settings for storage-constrained cluster"]

## Pre-Condition Check
- Memory status: [confirmed by user — e.g., "32 GiB total, ~20 GiB free"]
- Disk status: [confirmed by user — e.g., "500 GiB total, 60% used"]
- CPU status: [confirmed by user — e.g., "8 cores, average 40%"]

## Scope

| Parameter | Category | Trigger Condition | Reviewed |
|-----------|----------|-------------------|----------|
| ts.compress.stage | Compression Group | User wants compression optimization or smaller disk space usage | Y/N |
| ts.compress.algorithm | Compression Group | User wants compression optimization or smaller disk space usage | Y/N |
| ts.compress.level | Compression Group | User wants compression optimization or smaller disk space usage | Y/N |
| ts.rows_per_block.min_limit | Rows Per Block Group | User reports excessive small blocks from flushing, long write visibility delay, or high per-device data volume with low compression ratio | Y/N |
| ts.rows_per_block.max_limit | Rows Per Block Group | User reports excessive small blocks from flushing, long write visibility delay, or high per-device data volume with low compression ratio | Y/N |
| ts.compress.last_segment.enabled | Independent | User wants compression optimization or smaller disk space usage, or needs to optimize write performance | Y/N |
| ts.block.lru_cache.max_limit | Independent | User wants to optimize overall query performance, or memory usage is too high | Y/N |
| ts.last_cache_size.max_limit | Independent | User wants to optimize last-related SQL query performance, or memory usage is too high | Y/N |
| ts.mem_segment_size.max_limit | Independent | Write performance optimization (after ts.compress.last_segment.enabled reviewed), or memory usage is too high (after ts.block.lru_cache.max_limit and ts.last_cache_size.max_limit reviewed) | Y/N |
| ts.reserved_last_segment.max_limit | Independent | Frequent compaction triggers or disk space is tight | Y/N |
| ts.compact.max_limit | Independent | User reports compaction backlog with significant CPU idle, or CPU usage is too high | Y/N |
| ts.auto_vacuum.enabled | Independent | User wants to clean up data | Y/N |
| ts.block_filter.sampling_ratio | Independent | User reports poor query performance with range conditions or null checks, suspects inefficient filter pushdown | Y/N |

## Issues Found

| Setting | Current Value | Recommended Value | Reason | Risk |
|---------|---------------|-------------------|--------|------|
| `ts.xxx` | ... | ... | ... | ... |

## Recommended Changes

| Setting | SQL |
|---------|-----|
| `ts.xxx` | `SET CLUSTER SETTING ts.xxx = 'yyy';` |

## Expected Improvement
[What should change after applying the settings]

## Validation
```sql
SHOW CLUSTER SETTING ts.xxx;
```

## Notes
- Config suggestions only; execution requires user confirmation
- Compression changes affect new data only; existing data is not re-compressed
- Memory-related settings must not exceed available free memory
- Each recommended change must include the current value and the recommended value
- Each recommended change must explain why the change improves performance
- Reducing memory cache sizes (ts.block.lru_cache.max_limit, ts.last_cache_size.max_limit, ts.mem_segment_size.max_limit) may degrade query or write performance
- Reducing compression (ts.compress.stage, ts.compress.algorithm, ts.compress.level) to save CPU may increase disk space usage
