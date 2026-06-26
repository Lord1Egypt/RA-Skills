# 字节偏移游标 — 增量扫描实现

## 已集成 ✅

本功能已由 `scripts/scan_sessions_incremental.py` 原生实现，无需额外工作。

---

## 实现方式

### 状态文件

脚本自动维护 `memory/_state/scan_sessions_incremental.json`：

```json
{
  "version": 1,
  "files": {
    "dev:ino": {
      "offset": 4823456,
      "path": "~/.openclaw/agents/main/sessions/session-xxxx.jsonl",
      "size": 5234456,
      "mtime": 1713001234,
      "last_seen": "2026-04-15T15:30:00+00:00"
    }
  },
  "session_offsets": { "session-xxxx": 4823456 },
  "session_flags": { "session-xxxx": { "is_cron_session": false } }
}
```

### 增量扫描原理

1. 读取 `files[inode].offset`
2. `seek(offset)` 跳到上次位置
3. 只读**上次之后新增的完整行**（以 `\n` 结尾）
4. 更新 offset 为文件当前末尾

### Cron Session 识别

脚本扫描 session 前 4000 行，找第一条 user 消息：

```python
is_cron = text.lstrip().startswith("[cron:")
```

是 cron session → **跳过但更新 cursor**（避免重复扫描）

### 防半行 JSON

```python
if not line.endswith(b"\n"):
    break  # 不完整则等下次继续
```

## 关键设计

- **inode_key** 而非路径：文件被 rename/move 后仍可追踪
- **原子写入**：写 `.tmp` 再 rename，防止状态文件损坏
- **异常恢复**：状态文件损坏时自动重置 + warning

## 防套娃实现

脚本内部 `_should_ignore_text()` 实现：
- `NO_REPLY` → 忽略
- `memory-(hourly|daily|weekly) ok` → 忽略（正则）
- `System:` 前缀 → 忽略
- `[` 开头含 `Exec completed` / `A cron job` → 忽略
- `tool` / `system` role → 忽略
- tool_calls 消息 → 忽略

## 验证方法

```bash
# 查看统计
python3 scripts/scan_sessions_incremental.py --format json | \
  jq '.stats.messages_emitted, .stats.messages_ignored'

# 查看当前游标状态
cat memory/_state/scan_sessions_incremental.json | jq '.files'
```
