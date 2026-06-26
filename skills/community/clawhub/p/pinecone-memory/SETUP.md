# Pinecone Memory Setup

本文件提供可执行的最小接入流程，目标是 10 分钟内跑通：`check -> sync -> query -> stats`。

## 1. 前置条件

- Node.js 18+
- 有效的 Pinecone API Key
- 已创建 Integrated Embedding 索引（field_map 对应 `chunk_text`）

## 2. 安装依赖

在当前 skill 目录执行：

```bash
npm install
```

如果你只想手动安装核心依赖：

```bash
npm install @pinecone-database/pinecone
```

## 3. 设置环境变量

Windows PowerShell:

```powershell
$env:PINECONE_API_KEY="你的Key"
```

macOS/Linux:

```bash
export PINECONE_API_KEY="你的Key"
```

## 4. 创建或确认索引

本 skill 约定索引模型为 Integrated Embedding，写入字段为 `chunk_text`。

推荐索引参数：

- metric: `cosine`
- cloud/region: 按账号可用区选择（Starter 常见为 `aws/us-east-1`）
- embed.field_map: `chunk_text`

如果你已经有索引，可直接跳到下一步。

## 5. 运行最小闭环

### 5.1 环境与索引检查

```bash
node tools/pinecone-memory.mjs check --index openclaw-memory
```

### 5.2 同步本地记忆

```bash
node tools/pinecone-memory.mjs sync --index openclaw-memory --namespace default --path MEMORY.md --path memory --verify-write true
```

可选参数：

- `--chunk-size 800`
- `--max-chunks 200`
- `--dry-run`
- `--verify-write true|false`
- `--incremental true|false`（默认 true）
- `--state-file .pinecone-memory-state.json`
- `--record-type core_content|qa_knowledge|summary|entity_relation|conversation_history|agent_action|external_knowledge`
- `--tags 技术,产品A`
- `--author 张三 --department 平台组 --acl teamA --version v2`

### 5.3 语义检索验证

```bash
node tools/pinecone-memory.mjs query --index openclaw-memory --namespace default --text "用户偏好" --top-k 5
```

### 5.4 查看统计

```bash
node tools/pinecone-memory.mjs stats --index openclaw-memory --namespace default
```

### 5.5 心跳验证（推荐）

该命令会执行“写入探针 + 可见性校验”，可确认并非只调用 API，而是数据已在索引中可见。

```bash
node tools/pinecone-memory.mjs heartbeat --index openclaw-memory --namespace default --write-probe true
```

### 5.6 清理/备份/恢复

清理（危险操作，需确认）：

```bash
node tools/pinecone-memory.mjs cleanup --index openclaw-memory --namespace default --confirm yes
```

备份（导出为 JSONL）：

```bash
node tools/pinecone-memory.mjs backup --path MEMORY.md --path memory --output backup/pinecone-memory-backup.jsonl
```

恢复（从 JSONL 回写）：

```bash
node tools/pinecone-memory.mjs restore --input backup/pinecone-memory-backup.jsonl --index openclaw-memory --namespace default --verify-write true
```

## 6. 预期输出与验收标准

满足以下条件即为接入成功：

1. `check` 不报错，且能看到索引存在。
2. `sync` 输出 `upserted > 0`。
3. `sync` 输出 `writeVerification.verified = true`（开启 verify-write 时）。
3. `query` 返回至少 1 条命中。
4. `stats` 的向量数量与同步规模接近（允许短暂延迟）。
5. `heartbeat` 输出 `ok = true`。
6. 二次执行 `sync` 时 `skippedFiles > 0`（增量生效）。

## 7. HEARTBEAT / cron 优化建议

### 7.1 Linux/macOS cron

每 30 分钟巡检一次（写探针）：

```cron
*/30 * * * * cd /path/to/skill/memory && /usr/bin/node tools/pinecone-memory.mjs heartbeat --index openclaw-memory --namespace default --write-probe true >> logs/heartbeat.log 2>&1
```

每 6 小时做一次同步：

```cron
0 */6 * * * cd /path/to/skill/memory && /usr/bin/node tools/pinecone-memory.mjs sync --index openclaw-memory --namespace default --path MEMORY.md --path memory --verify-write true >> logs/sync.log 2>&1
```

### 7.2 Windows 任务计划（Task Scheduler）

程序：`node`
参数：`tools/pinecone-memory.mjs heartbeat --index openclaw-memory --namespace default --write-probe true`
起始于：skill 目录

建议：
- 高频巡检：每 30 分钟执行 heartbeat。
- 低频同步：每 6 小时执行 sync。

## 8. 常见错误处理

- `PINECONE_API_KEY is not set`
  - 原因：环境变量未设置或当前 shell 未生效。
  - 处理：重新设置变量并在同一 shell 重试。

- `Index not found`
  - 原因：索引名错误或索引不在当前项目/区域。
  - 处理：确认索引名与控制台一致。

- `Integrated embedding search API is not available`
  - 原因：当前 SDK 版本缺少 `searchRecords`。
  - 处理：升级 Pinecone SDK 后重试。

- 写后立即查不到
  - 原因：Pinecone 最终一致性。
  - 处理：等待几秒后重试查询。

## 9. 重要约束

- 使用 Integrated Embedding 时，不要手动传向量。
- 写入记录必须包含 `chunk_text` 字段。
- 建议将测试和生产分别写入不同 namespace。
