# hipool — Hippocampal Memory Pool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![C](https://img.shields.io/badge/language-C-blue.svg)
![Size](https://img.shields.io/badge/binary-39KB-brightgreen)

**An embedded memory engine for AI agents, edge devices, and resource-constrained systems.**

Inspired by the hippocampal-cortical dual storage model of the human brain. Zero external dependencies — just libc and a C compiler.

---

## Why hipool?

|                 Problem                  |             What hipool does              |
|------------------------------------------|-------------------------------------------|
| Redis/SQLite too heavy for embedded      | **39KB binary, 2MB fixed memory pool**    |
| Database latency too high for hot data   | **~650ns median SET, ~4.5μs median GET**  |
| Agent memory needs controlled forgetting | **LRU day-level eviction with 7-day TTL** |
| Crash safety in unreliable environments  | **Atomic rename writes (tmp + rename)**   |
| Need tag-based retrieval, not just KV    | **Built-in inverted tag index**           |

---

## Quick Start

```bash
git clone https://github.com/hualang-C/Hipool
cd hipool
gcc -O2 memory.c -o memory
./memory set "2026-06-03-01" "hipool initialized" --tags "system,startup"
./memory get "2026-06-03-01"
./memory search --tag "startup"
./memory stats
```

---

## Commands

```
memory set     <key> <value> [--tags a,b,c] [--ts <unix_sec>]    Store
memory get     <key>                                                 Read
memory del     <key>                                                 Delete
memory search  <query>                                               Text search
memory search  --tag <tag>                                           Tag search
memory search  --date YYYY-MM-DD                                     Date search
memory flush                                                         Write snapshot
memory load                                                          Load from disk
memory clean                                                         Purge expired files
memory stats                                                         Pool status
```

---

## Architecture

```
┌───────────────────────────────────────────────────┐
│                  CLI  (CLI layer)                 │
├───────────────────────────────────────────────────┤
│             Public API  (memory_set/get/search)   │
├───────────────────────────────────────────────────┤
│  ┌─────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │  Hash   │  │   Tag    │  │   Memory Pool    │  │
│  │  Table  │  │  Index   │  │  (Slab Alloc)    │  │
│  │  (djb2) │  │ (invert) │  │ 4 levels:        │  │
│  │ 4096 bkt│  │ 512 bkt  │  │ 256/1K/4K/16K    │  │
│  └────┬────┘  └────┬─────┘  └────────┬─────────┘  │
│       └──────┬─────┘                 │            │
│              ▼                       ▼            │
│       ┌────────────────────────────────┐          │
│       │     Overflow Manager           │          │
│       │  (evict, flush, load, clean)   │          │
│       └──────────────┬─────────────────┘          │
├──────────────────────┼────────────────────────────┤
│                      ▼                            │
│         memory_data/memory_snapshot.json          │
│         memory_data/memory-YYYY-MM-DD.json        │
└───────────────────────────────────────────────────┘
```

### Hippocampal-Cortex Model

|       Component      |       Brain Analogy      |        hipool Implementation        |
|----------------------|--------------------------|-------------------------------------|
| Hot memory pool      | Hippocampus (short-term) | 2MB slab allocator, μs latency      |
| Daily overflow files | Neocortex (long-term)    | Day-split JSON, lazy reload         |
| Day-level eviction   | Sleep consolidation      | Oldest day evicted at 80% watermark |
| Tag index            | Associative recall       | Inverted tag → entry links          |

---

## Performance

Measured on AMD EPYC 7K62 @ 2.6GHz, 32B values, 50K entries:

|         Metric         |           Value            |
|------------------------|----------------------------|
| SET p50                | **~650 ns**                |
| GET p50                | **~4.5 μs**                |
| SET p99                | **~1.9 μs**                |
| Mixed (70%R/30%W)      | **~255,000 ops/s**         |
| Binary size (stripped) | 39 KB                      |
| Runtime memory         | 2 MB (fixed, configurable) |
| Disk per entry         | ~1-2 KB                    |

All 30 test cases pass. Zero segfaults. Zero memory leaks.

---

## Crash Safety

All disk writes follow a **temp file → atomic rename** pattern. If power is lost mid-write, the old data remains intact. Dual canary markers (`0xDEADBEEB`) around each entry detect memory corruption on `pool_free`.

---

## Configuration (compile-time constants in `memory.c`)

|     Constant    | Default |              Description                |
|-----------------|---------|-----------------------------------------|
| `POOL_SIZE`     | 2 MB    | Fixed memory pool size                  |
| `MAX_VAL_LEN`   | 16320   | Max value length per entry              |
| `LOW_WATER`     | 80%     | Eviction trigger threshold              |
| `FILE_TTL_DAYS` | 7       | Days before historical files are purged |

---

## Building

```bash
# Standard — single thread, zero overhead
gcc -O2 memory.c -o memory

# Thread-safe
gcc -O2 -DHIPOOL_USE_MUTEX -lpthread memory.c -o memory

# Tests
gcc -O2 -DTEST_MODE memory.c -o memory_test
./test.sh
```

---

## License

MIT

---

## Citation (if used in research)

```bibtex
@software{hipool2026,
  title        = {hipool: An Embedded Memory Engine for AI Agents},
  author       = {hipool contributors},
  year         = {2026},
  url          = {https://github.com/hualang-C/Hipool}
}
```
