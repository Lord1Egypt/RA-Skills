# Pinecone Heartbeat and Cron

本文用于保障两个目标：

1. 定期确认 Pinecone 链路可用。
2. 定期确认写入不是“假成功”，而是可见。

## 推荐命令

### 心跳巡检（写探针 + 可见性验证）

```bash
node tools/pinecone-memory.mjs heartbeat --index openclaw-memory --namespace default --write-probe true
```

成功标志：

- 输出 `ok: true`
- `probe.verified: true`
- `delta >= 1`

### 定期同步（带写后验证）

```bash
node tools/pinecone-memory.mjs sync --index openclaw-memory --namespace default --path MEMORY.md --path memory --verify-write true
```

建议保持 `--incremental true`（默认值），减少重复写入和 API 成本。

### 管理命令

清理命令（危险，需确认）：

```bash
node tools/pinecone-memory.mjs cleanup --index openclaw-memory --namespace default --confirm yes
```

备份命令：

```bash
node tools/pinecone-memory.mjs backup --path MEMORY.md --path memory --output backup/pinecone-memory-backup.jsonl
```

恢复命令：

```bash
node tools/pinecone-memory.mjs restore --input backup/pinecone-memory-backup.jsonl --index openclaw-memory --namespace default --verify-write true
```

成功标志：

- `upserted > 0`
- `writeVerification.verified: true`

## 频率建议

- 高频检查：每 30 分钟执行 heartbeat。
- 低频同步：每 6 小时执行 sync。

## cron 示例（Linux/macOS）

```cron
*/30 * * * * cd /path/to/skill/memory && /usr/bin/node tools/pinecone-memory.mjs heartbeat --index openclaw-memory --namespace default --write-probe true >> logs/heartbeat.log 2>&1
0 */6 * * * cd /path/to/skill/memory && /usr/bin/node tools/pinecone-memory.mjs sync --index openclaw-memory --namespace default --path MEMORY.md --path memory --verify-write true >> logs/sync.log 2>&1
```

## Windows 任务计划

任务 1（心跳）：

- 程序：`node`
- 参数：`tools/pinecone-memory.mjs heartbeat --index openclaw-memory --namespace default --write-probe true`
- 起始于：当前 skill 目录
- 触发器：每 30 分钟

任务 2（同步）：

- 程序：`node`
- 参数：`tools/pinecone-memory.mjs sync --index openclaw-memory --namespace default --path MEMORY.md --path memory --verify-write true`
- 起始于：当前 skill 目录
- 触发器：每 6 小时

## 告警建议

当下列任一条件满足时应告警：

- heartbeat 返回 `ok: false`
- heartbeat `probe.verified: false`
- sync `writeVerification.verified: false`
- 连续两次 query 命中为 0（对稳定查询词）
