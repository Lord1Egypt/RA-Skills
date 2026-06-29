# hipool — Embedded Memory Engine for AI Agents v1.0.0

> Hippocampal-cortex dual storage model · Pure C · Zero external dependencies (libc only)
> Codename: hipool (Hippocampus + Memory Pool)

A lightweight, embedded memory engine designed for AI agents, edge devices, and resource-constrained environments. Inspired by how the human brain stores and retrieves information through the hippocampal-cortical dual storage system.

---

## Quick Start

```bash
gcc -O2 memory.c -o memory

# Store
./memory set "today weather" "sunny" --tags weather,beijing
# Read
./memory get "today weather"
# Tag search
./memory search --tag weather
# Time range query
./memory search --range 1717920000 1718006400
# Date query
./memory search --date 2026-06-08
# List all shards
./memory shard list
# Store to specific shard
./memory set key val --shard people
# Fork snapshot (BGSAVE style)
./memory snapshot
# View status
./memory stats
```

---

## Core Features

### 1. Slab Allocator (2MB pool)
- Four fixed-size classes: 256B (793 slots) / 1K (406) / 4K (153) / 16K (51)
- Bitmap-based free tracking + canary overflow detection
- Automatic fallback to higher class when current is full
- 80% watermark triggers eviction (flush to disk, then free memory)

### 2. Triple Index
- **Hash Table** (DJB2, 4096 buckets): O(1) key-value lookup
- **Tag Inverted Index** (512 buckets): tag → entry mapping, dynamic expansion
- **SkipList Sorted Index** (14 levels): compound sort by `created_at + key_hash`, O(log n) insert/delete/range query

### 3. WAL (Write-Ahead Log)
- Binary append-only `memory_data/wal.log`
- Every SET/DEL writes WAL before modifying in-memory data
- Automatic `wal_replay` on startup to recover unflushed data
- WAL disabled during load to prevent recursive writes

### 4. Named Shards
- Each shard has its own Pool / Hash Table / Tag Index / SkipList / WAL
- 256KB pool per shard, max 8 named shards
- `--shard <name>` routes operations to the specified shard
- Automatic discovery of existing shard directories
- Independent persistence: `data_dir/shard_<name>/`

### 5. Fork Snapshot (BGSAVE style)
- `memory snapshot`: forks a child process for COW-consistent snapshot
- Flushes all shards simultaneously
- Parent process stays unblocked (zero-downtime checkpointing)
- Safely rejects when compiled with mutex mode (fork + mutex is unsafe)

### 6. Thread Safety
- Compile with `-DHIPOOL_USE_MUTEX -lpthread` to enable
- Per-context independent mutex (not global)
- All public APIs protected by locks
- Defaults to NOP (zero overhead) when mutex is disabled

---

## Command Reference

```bash
# Data operations
memory set <key> <value> [--tags a,b,c] [--ts <unix_sec>] [--shard <name>]
memory get <key> [--shard <name>]
memory del <key> [--shard <name>]

# Search
memory search <keyword> [--shard <name>]
memory search --tag <tag> [--shard <name>]
memory search --date YYYY-MM-DD [--shard <name>]
memory search --range <start_ts> <end_ts> [--shard <name>]

# Management
memory shard list|create <name>
memory flush             # Full snapshot write (all shards)
memory snapshot          # Fork snapshot
memory load              # Restore from disk
memory clean             # Purge expired files
memory stats             # View status
```

---

## Compilation

```bash
# Standard (single-thread)
gcc -O2 memory.c -o memory
strip memory  # 52KB → ~42KB

# Multi-thread
gcc -O2 -DHIPOOL_USE_MUTEX memory.c -o memory_mt -lpthread
```

---

## Project Structure

```
hipool/
├── memory              ← 52KB single binary
├── memory.c            ← Source code
├── memory_data/        ← Runtime data directory
│   ├── memory_snapshot.json   ← JSON snapshot
│   ├── wal.log                ← Write-ahead log
│   └── shard_<name>/          ← Named shard data
├── CHANGELOG.md        ← Version history
├── SKILL.md            ← This file
├── benchmark_results.md    ← Performance comparison
├── ablation_test.sh    ← Ablation test script
├── test.sh             ← Test suite
├── bench_compare.c     ← Comparison benchmark
└── bench_small.c       ← Pool benchmark
```

---

## Performance (Measured on AMD EPYC 7K62, Tencent Cloud)

### In-pool (no eviction)

| Operation |   32B    | 256B  |    1KB    |  4KB  |
|-----------|----------|-------|-----------|-------|
| SET avg   | 1.7μs    | 1.9μs | 3.2μs     | 4.4μs |
| SET p50   | 1.5μs    | 1.5μs | 2.7μs     | 4.1μs |
| GET avg   | **55ns** | 62ns  | **55ns**  | 67ns  |
| GET p50   | **50ns** | 60ns  | **50ns**  | 60ns  |

### vs LMDB / SQLite / Redis (in-pool GET)

|  Database  |      32B      |      256B     |      1KB      |      4KB      |
|------------|---------------|---------------|---------------|---------------|
| **hipool** | **55ns**      | **62ns**      | **55ns**      | **67ns**      |
| LMDB       | 936ns (17x)   | 937ns (15x)   | 1.0μs (19x)   | 1.4μs (21x)   |
| SQLite     | 6.6μs (120x)  | 6.8μs (109x)  | 10μs (180x)   | 8.8μs (131x)  |
| Redis      | 326μs (5900x) | 332μs (5350x) | 332μs (6000x) | 352μs (5250x) |

### Scale test (N=50000, with eviction)

| Database | SET 32B avg | GET 32B avg | Binary size | Resident memory |
|----------|-------------|-------------|-------------|-----------------|
| hipool   | 8.8μs       | 337μs       | **52KB**    | **2MB**         |
| LMDB     | 1.5μs       | 0.9μs       | 2MB+        | 1GB             |
| SQLite   | 2.9μs       | 7.1μs       | .so         | file            |
| Redis    | 327μs       | 326μs       | 20MB        | memory          |

### Ablation Tests

**40/40 all passed ✅**:
- SkipList: 20 same-timestamp collisions ✓ · empty range ✓ · huge range ✓ · delete-all-then-range ✓
- Large data: 500 batch insert ✓ · sort order ✓ · delete 250 query 250 ✓
- WAL: basic recovery ✓ · 100 entries single-process ✓ · DEL recovery ✓ · corrupted WAL no crash ✓
- Shard: 5-way isolation ✓ · default no leak ✓ · overflow rejected ✓ · range query ✓ · flush+reload ✓
- Fork Snapshot: basic ✓ · concurrent writes ✓ · shard+snapshot ✓
- Comprehensive bounds: Chinese keys ✓ · emoji ✓ · 255-byte key ✓ · empty value ✓ · 16KB value ✓ · 16 tags ✓ · time range ✓ · Mutex mode ✓

---

## Configuration (compile-time constants in memory.c)

|       Constant      | Default |        Description         |
|---------------------|---------|----------------------------|
| `POOL_SIZE`         | 2MB     | Main memory pool size      |
| `SHARD_POOL_SIZE`   | 256KB   | Per-shard pool size        |
| `MAX_KEY_LEN`       | 256     | Max key length             |
| `MAX_VAL_LEN`       | 16320   | Max value length           |
| `MAX_TAGS`          | 16      | Max number of tags         |
| `MAX_TAG_LEN`       | 64      | Max tag length             |
| `EVICT_WATER`       | 80%     | Eviction trigger watermark |
| `FILE_TTL_DAYS`     | 7       | Disk file retention days   |
| `SL_PROB`           | 4 (1/4) | SkipList level probability |
| `MAX_SHARDS`        | 8       | Max named shards           |

---

## Resource Usage

|          Metric         |                        Value                       |
|-------------------------|----------------------------------------------------|
| Binary size             | 52KB (strip ~42KB)                                 |
| Runtime memory          | 2MB fixed (+ shard × 256KB)                        |
| Thread-safe version     | 58KB (+6KB pthread)                                |
| Lines of code           | 1642 C                                             |
| External deps           | 0 (libc only)                                      |
| Write latency (in-pool) | 1.5-4.4μs                                          |
| Read latency (in-pool)  | **50-67ns**                                        |
| In-pool capacity        | ~1400 (32B) / ~610 (256B) / ~200 (1KB) / ~50 (4KB) |
| Disk usage              | ~1-2KB/entry (JSON)                                |

---

## Troubleshooting

```bash
./memory stats               # Check memory usage
./memory load                # Reload from disk
ls memory_data/              # View disk files
cat memory_data/memory_snapshot.json  # View snapshot content
xxd memory_data/wal.log      # View WAL content
```

---

## See Also

- Performance report: `benchmark_results.md`
- Ablation script: `ablation_test.sh`
- Test suite: `test.sh`
- Changelog: `CHANGELOG.md`
