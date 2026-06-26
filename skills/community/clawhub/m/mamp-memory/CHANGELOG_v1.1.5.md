# AI Memory Protocol — v1.1.5

**文件**: `ai_memory_protocol_v1.1.5.py`  
**协议版本**: `PROTOCOL_VERSION = "1.1.5"`  
**数据库版本**: `DB_VERSION = 14`  
**状态**: 测试通过，已部署  
**Cron**: `e9805661b493` → 每 30 分钟 recall

---

## 新增功能

### 1. priority_levels 持久化到 DB
`add_priority_level()` 和 `remove_priority_level()` 现在写入 DB，重启后仍然有效。

### 2. merge_sessions duplicate O(n log n)
用 bisect 优化冲突检测，从 O(n²) 降到 O(n log n)。

### 3. vacuum() 增强参数
- `batch_size` — 每批提交行数
- `compress_level` — zlib 压缩级别（默认 6，原先是 1）
- `max_memory_mb` — 内存限制

### 4. FTS 重建线程锁
`_fts_ensure()` 加锁，防止并发重建。

### 5. search_batch daemon threads
线程设为 daemon，主进程退出时自动清理。

### 6. busy_timeout=5000
所有写连接加 PRAGMA busy_timeout，防止锁冲突。

---

## Bug Fix

### _fts_lock 未定义
`_rebuild_fts()` 里引用了 `_fts_lock`，但 `import threading` 在文件底部，锁也从未初始化。修复：lazy init。

### search() FTS 路径 — tags 混合类型
FTS 返回的 `r.get("tags")` 是 Python list，直接查 DB 是 JSON 字符串。
修复：统一用 `isinstance` 判断后做相应解析。

### SessionManager.search_count() — tag_filter list 归一化
接口是 `tag_filter: Optional[str]`，但调用方传 list。修复：在 wrapper 层把 `['finance']` 转为 `'finance'`。

### REVERT — tag_filter 精确匹配逻辑
v1.1.5 改进的精确匹配（`tags=? OR tags LIKE ...`）反而破坏了原有工作场景（finance 作为第一个 JSON 元素时 LIKE 匹配失败）。
修复：还原 v1.1.4 的简单 `LIKE '%"finance"%'` 逻辑。

---

## 集成测试结果

```
search_count(finance)=1    ✅ PASS
search_count(glass)=1      ✅ PASS
get_session_extended()     ✅ total_turns=2
vacuum(squash_spaces=True) ✅ True
priority persist           ✅ critical survives restart
tag_filter list→str       ✅ ['finance'] → 1 result
```

---

## 文件结构

```
/opt/claw/hermes/protocol/
├── ai_memory_protocol_v1.1.5.py    ← 当前版本
├── ai_memory_protocol_v1.1.4.py     ← 上一版本
├── ai_memory_protocol_v1.1.2.py     ← Leo 重命名版（内容同 v1.1.4）
├── CHANGELOG_v1.1.5.md              ← 本文档
├── CHANGELOG_v1.1.4.md              ← 上一版本 changelog
├── mark_memory.db                   ← 实际数据库
└── backups/
    ├── 20260416_v111_bugfix/
    └── 20260417_v114_final/
```
