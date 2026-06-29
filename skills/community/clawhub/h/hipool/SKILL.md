# hipool — 嵌入式 AI Agent 记忆系统 v4.5

> 海马体-皮层双存储模型 · 纯 C · 零外部依赖 (libc only)
> 项目代号 hipool (海马体 + 资源池 + 河马)

## 快速开始

```bash
cd skills/memory-c
gcc -O2 memory.c -o memory

# 存储
./memory set "今天天气" "晴天" --tags weather,北京
# 读取
./memory get "今天天气"
# 按标签搜索
./memory search --tag weather
# 时间范围查询
./memory search --range 1717920000 1718006400
# 按日期查询
./memory search --date 2026-06-08
# 列出所有分片
./memory shard list
# 写入指定分片
./memory set key val --shard people
# Fork 快照（BGSAVE 风格）
./memory snapshot
# 查看状态
./memory stats
```

## 核心功能 (v4.5)

### 1. Slab 分配器 (2MB 池)
- 四级: 256B(793 slot) / 1K(406) / 4K(153) / 16K(51)
- Bitmap 空闲追踪 + canary 溢出检测
- 同级满时自动 fallback 更高级别
- 水位 80% 触发 eviction → 写盘后释放

### 2. 三重索引
- **Hash 表** (DJB2, 4096 桶): O(1) 键值查找
- **Tag 倒排索引** (512 桶): tag → 条目映射，动态扩容
- **SkipList 排序索引** (14 层): 按 `created_at + key_hash` 复合排序，O(log n) 插入/删除/范围查询

### 3. WAL 预写日志 (v4.3)
- 二进制追加写 `memory_data/wal.log`
- 每次 SET/DEL 先写 WAL 再改内存
- 崩溃后自动 `wal_replay` 恢复未落盘数据
- 加载阶段 `wal_disabled=1` 防止递归写

### 4. Shard 命名分片 (v4.4)
- 每个 shard 独立 Pool/Hash/Tag/SkipList/WAL
- 256KB 小池 · 最多 8 个命名分片
- `--shard <name>` 路由操作 · 自动发现已有目录
- 独立持久化: `data_dir/shard_<name>/`

### 5. Fork 快照 (v4.5)
- `memory snapshot`: fork 子进程写快照 (COW)，父进程不阻塞
- 同时 flush 所有 shard
- 多线程模式下安全拒绝 (fork+mutex 不安全)

### 6. 线程安全 (v4.5)
- 编译 `-DHIPOOL_USE_MUTEX -lpthread` 激活
- per-ctx 独立 mutex，默认 NOP 零开销
- 所有公开 API 加锁保护

## 命令参考

```bash
# 数据操作
memory set <key> <value> [--tags a,b,c] [--ts <unix_sec>] [--shard <name>]
memory get <key> [--shard <name>]
memory del <key> [--shard <name>]

# 搜索
memory search <关键词> [--shard <name>]
memory search --tag <标签> [--shard <name>]
memory search --date YYYY-MM-DD [--shard <name>]
memory search --range <start_ts> <end_ts> [--shard <name>]

# 管理
memory shard list|create <name>
memory flush           # 全量写快照 (含所有 shard)
memory snapshot        # Fork 快照
memory load            # 从磁盘恢复
memory clean           # 清理过期文件
memory stats           # 查看状态
```

## 编译选项

```bash
# 标准版 (单线程)
gcc -O2 memory.c -o memory
strip memory  # 52KB → ~42KB

# 多线程版
gcc -O2 -DHIPOOL_USE_MUTEX memory.c -o memory_mt -lpthread
```

## 源码结构

```
skills/memory-c/
├── memory             ← 52KB 单二进制
├── memory.c           ← 1642 行 C 源码
├── memory_data/       ← 运行时数据目录
│   ├── memory_snapshot.json   ← JSON 快照
│   ├── wal.log                ← WAL 预写日志
│   └── shard_<name>/          ← 命名分片数据
├── CHANGELOG.md       ← 版本日志
├── SKILL.md           ← 本文件
├── benchmark_results.md  ← 性能对比报告
├── ablation_test.sh   ← 消融测试脚本
├── test.sh            ← 原测试套件
├── bench_compare.c    ← 对比基准
└── bench_small.c      ← 池内基准
```

## 性能数据 (实测, 腾讯云 AMD EPYC 7K62)

### 池内 (无 eviction)

|operation|    32B    | 256B  |    1KB    |  4KB  |
|---------|-----------|------ |-----------|-------|
| SET avg | 1.7μs     | 1.9μs | 3.2μs     | 4.4μs |
| SET p50 | 1.5μs     | 1.5μs | 2.7μs     | 4.1μs |
| GET avg | **55ns**  | 62ns  | **55ns**  | 67ns  |
| GET p50 | **50ns**  | 60ns  | **50ns**  | 60ns  |

### 与 LMDB/SQLite/Redis 对比 (池内 GET)

|  database  |     32B    |   256B   |    1KB    |   4KB    |
|------------|------------|----------|-----------|----------|
| **hipool** | **55ns**   | **62ns** | **55ns**  | **67ns** |
| LMDB       | 936ns      | 937ns    | 1.0μs     | 1.4μs    |
| SQLite     | 6.6μs      | 6.8μs    | 10μs      | 8.8μs    |
| Redis      | 326μs      | 332μs    | 332μs     | 352μs    |

### 规模数据 (N=50000, 含 eviction)

| database | SET 32B avg | GET 32B avg |   bin    | residentmemory |
|----------|-------------|-------------|----------|----------------|
| hipool   | 8.8μs       | 337μs       | **52KB** | **2MB**        |
| LMDB     | 1.5μs       | 0.9μs       | 2MB+     | 1GB            |
| SQLite   | 2.9μs       | 7.1μs       | DLL      | file           |
| Redis    | 327μs       | 326μs       | 20MB     | memory         |

### 消融实验

**40/40 全部通过 ✅**：
- SkipList: 同时间戳碰撞 20 条 ✓ · 空范围 ✓ · 超大范围 ✓ · 删光后范围 ✓
- 大量数据: 500 条批量 ✓ · 排序顺序 ✓ · 删 250 查 250 ✓
- WAL: 基本恢复 ✓ · 100 条单进程恢复 ✓ · DEL 恢复 ✓ · 损坏 WAL 不崩溃 ✓
- Shard: 5 个隔离 ✓ · 默认无泄漏 ✓ · 超限拒绝 ✓ · 范围查询 ✓ · flush+reload ✓
- Fork Snapshot: 基本 ✓ · 并发写入 ✓ · shard+snapshot ✓
- 综合边界: 中文 key ✓ · emoji ✓ · 255B key ✓ · 空 value ✓ · 16KB value ✓ · 16 标签 ✓ · 时间范围 ✓ · Mutex 版 ✓

## 与 OpenClaw 集成

```bash
# cron 任务: 定时记忆同步
openclaw cron add --schedule "0 * * * *" \
  --account <bot_id> --to <user_id> \
  --exec 'cd skills/memory-c && ./memory set "YYYY-MM-DD" "摘要" --tags "标签1,标签2"'

# 检索记忆
./memory search --tag <标签> [--shard <name>]
./memory search --range <start> <end> [--shard <name>]
```

## 配置常量 (编译前修改 memory.c 顶部)

| 常量 | 默认值 | 说明 |
|------|:------:|------|
| `POOL_SIZE` | 2MB | 主内存池大小 |
| `SHARD_POOL_SIZE` | 256KB | 每个 shard 池大小 |
| `MAX_KEY_LEN` | 256 | 最大 key 长度 |
| `MAX_VAL_LEN` | 16320 | 最大 value 长度 |
| `MAX_TAGS` | 16 | 最大标签数 |
| `MAX_TAG_LEN` | 64 | 单个标签最大长度 |
| `EVICT_WATER` | 80% | 触发逐出水位 |
| `FILE_TTL_DAYS` | 7 | 磁盘文件保留天数 |
| `SL_PROB` | 4 (1/4) | SkipList 层级概率 |
| `MAX_SHARDS` | 8 | 最大命名分片数 |

## 资源占用

| 指标 | 值 |
|------|-----|
| 二进制大小 | 52KB (strip 后 ~42KB) |
| 运行时内存 | 2MB 固定 (+ shard × 256KB) |
| 线程安全版 | 58KB (+6KB pthread) |
| 代码行数 | 1642 行 C |
| 外部依赖 | 0 (libc only) |
| 写入延迟 (池内) | 1.5-4.4μs |
| 读取延迟 (池内) | **50-67ns** 🔥 |
| 池内容量 | ~1400 条 (32B) / ~610 条 (256B) / ~200 条 (1KB) / ~50 条 (4KB) |
| 磁盘占用 | ~1-2KB/条目 (JSON) |

## 版本历史

| 版本 | 日期 | 新增 |
|:----:|:----:|------|
| v4.5 | 2026-06-08 | 线程安全 (per-ctx mutex) · Fork 快照 (BGSAVE) · eviction 修复(sl_remove) |
| v4.4 | 2026-06-08 | Shard 命名分片 · `--shard <name>` 路由 · 自动发现 · stats 增强 |
| v4.3 | 2026-06-08 | SkipList 排序索引 · `--range` 范围查询 · WAL 预写日志 · 崩溃恢复 |
| v4.2 | 2026-06-02 | `--ts` 自定义时间戳 |
| v4.1 | 2026-05-30 | 崩溃安全写入 · 可选多线程 · canary 检测 · 去重优化 |
| v4.0 | 2026-05-28 | 首次稳定版: Slab · Hash · Tag · 日文件溢出 · 惰性加载 |

## 故障排查

```bash
./memory stats               # 查看内存使用率
./memory load                # 从磁盘重新加载
ls memory_data/              # 查看磁盘文件
cat memory_data/memory_snapshot.json  # 查看快照内容
xxd memory_data/wal.log      # 查看 WAL 内容
```

## 相关文档

- 性能报告: `benchmark_results.md`
- 架构图: hipool_architecture_v4.5.jpg
- 消融脚本: `ablation_test.sh`
- 原测试套件: `test.sh`

> 弃用了 Redis v3.2.3 记忆系统 (2026-05-29 清除)，全面切换至 hipool C 内存系统。
