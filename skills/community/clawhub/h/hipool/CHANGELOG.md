# Changelog

## v4.5 (2026-06-08)
- 线程安全: `-DHIPOOL_USE_MUTEX -lpthread` 编译时启用
  - per-ctx 独立 mutex (非全局)
  - 所有公开 API 加锁保护
  - `memory_fork_snapshot()` 检测线程模式后安全拒绝
- Fork 快照: `memory snapshot` 命令
  - fork 子进程, COW 一致性快照
  - 同时 flush 所有 shard
  - 父进程不阻塞, 子进程写完即退
  - 自动关闭子进程继承的 fd
- stats 只读操作不加锁 (const MemoryCtx*)

## v4.4 (2026-06-08)
- Shard 分区: 命名分片，独立 Pool/HashTable/TagIndex/SkipList
- `memory shard list` — 列出所有 shard
- `--shard <name>` — 路由操作到指定 shard (set/get/search/del)
- 自动发现已有 shard 目录 (`shard_<name>/`) 并加载
- 每个 shard 256KB 小池 + 独立 WAL + 独立快照
- stats 显示 shard 列表与条目数
- `--tag` 别名支持 (与 `--tags` 等价)

## v4.3 (2026-06-08)
- SkipList 排序索引 (按 created_at + key_hash 复合排序)
- `memory search --range <start_ts> <end_ts>` 时间范围查询
- `memory search --date` 内部走 SkipList (O(log n + k))
- WAL 预写日志 (memory_data/wal.log, 二进制追加)
- 崩溃恢复: 启动时 wal_replay 自动恢复未落盘数据
- WAL 禁用标志防止加载/重播时递归写入
- stats 显示 Sorted idx 条目数

## v4.2 (2026-06-02)
- `--ts` parameter for `memory set` to specify custom timestamps

## v4.1 (2026-05-30)
- Crash-safe disk writes (temp file + atomic rename)
- Optional thread safety (`-DHIPOOL_USE_MUTEX -lpthread`)
- Timestamp preservation on disk reload
- Tail canary detection on `pool_free`
- Dedup optimization (only checks last 10 entries)

## v4.0 (2026-05-28)
- First stable release
- Slab-based memory pool (2MB)
- DJB2 hash table + inverted tag index
- Day-level overflow with eviction
- Lazy disk scan for historical data
