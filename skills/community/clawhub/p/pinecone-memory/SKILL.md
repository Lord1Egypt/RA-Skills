---
name: memory
description: 使用 Pinecone 作为 OpenClaw 语义记忆后端，支持记忆同步(sync)、语义检索(query)和统计(stats)。Use when: 用户要求把本地记忆同步到 Pinecone、查询历史语义记忆、验证索引状态或排查 Pinecone 记忆链路问题。
metadata: {"openclaw":{"primaryEnv":"PINECONE_API_KEY","requires":{"env":["PINECONE_API_KEY"],"bins":["node"]}}}
---

# Pinecone Memory Skill

这个 skill 提供一个最小可运行的 Pinecone 记忆工具链：

- `check`：检查环境变量与索引可用性。
- `sync`：把本地 markdown 记忆切片后写入 Pinecone。
- `query`：按文本做语义检索（优先走 Integrated Embedding 搜索接口）。
- `stats`：查看索引和命名空间统计。
- `heartbeat`：写入探针并验证写入可见性，用于健康检查与定时巡检。
- `cleanup`：清理指定 namespace 的数据。
- `backup` / `restore`：本地 JSONL 备份与恢复。

本 skill 采用 Integrated Embedding 索引（记录里必须有 `chunk_text`），默认不手动传向量。

## 触发时机

- 用户说“把记忆同步到 Pinecone”。
- 用户说“查一下以前关于 X 的记忆”。
- 用户说“看下 Pinecone 是否正常 / 有多少数据”。

## 执行流程（必须按顺序）

1. 先跑环境检查：

```bash
node {baseDir}/tools/pinecone-memory.mjs check --index openclaw-memory
```

2. 再做同步：

```bash
node {baseDir}/tools/pinecone-memory.mjs sync --index openclaw-memory --namespace default --path MEMORY.md --path memory
```

默认开启增量同步（基于本地状态文件比对 source hash，仅写入变化文件）。

3. 再做查询验证：

```bash
node {baseDir}/tools/pinecone-memory.mjs query --index openclaw-memory --namespace default --text "用户偏好"
```

4. 最后看统计：

```bash
node {baseDir}/tools/pinecone-memory.mjs stats --index openclaw-memory --namespace default
```

5. 健康巡检（验证“真的写入”）：

```bash
node {baseDir}/tools/pinecone-memory.mjs heartbeat --index openclaw-memory --namespace default --write-probe true
```

6. 管理命令：

```bash
node {baseDir}/tools/pinecone-memory.mjs cleanup --index openclaw-memory --namespace default --confirm yes
node {baseDir}/tools/pinecone-memory.mjs backup --path MEMORY.md --path memory --output backup/pinecone-memory-backup.jsonl
node {baseDir}/tools/pinecone-memory.mjs restore --input backup/pinecone-memory-backup.jsonl --index openclaw-memory --namespace default --verify-write true
```

## 存储信息模型（必须覆盖）

1. 核心内容（向量主体）
- 文档/知识库分块、网页分块、书籍/报告/论文分块、代码片段与 API 文档。
- 写入字段：`chunk_text`（Integrated Embedding 主字段）。

2. 元数据（过滤与追溯）
- 来源：`source`、`source_url`。
- 时间：`created_at`、`updated_at`。
- 作者与部门：`author`、`department`。
- 标签与分类：`tags`、`source_kind`。
- 权限：`acl_scope`。
- 版本：`doc_version`。

3. 结构化知识块
- 记录类型通过 `record_type` 区分：`core_content`、`qa_knowledge`、`summary`、`entity_relation`、`conversation_history`、`agent_action`、`external_knowledge`、`heartbeat`。

4. 对话与交互历史
- 历史对话、Agent 行动日志可作为 `record_type` 写入同一索引，按 namespace 隔离。

5. 外部与实时信息
- API 返回摘要、用户临时上传文件解析文本可作为短时记忆写入，建议使用单独 namespace 并定期清理。

## 行为规则

1. 同步前先过滤明显敏感内容（如 API key、token、密码字段）。
2. 统一使用结构化 `_id`，格式为 `source#chunk-<n>#<hash8>`。
3. 命名空间默认 `default`，生产与测试必须分离。
4. 查询返回只保留高相关结果，默认 `topK=5`。
5. `sync` 默认开启写后可见性校验，输出 `writeVerification`。
6. `sync` 默认开启增量同步，状态保存在 `.pinecone-memory-state.json`。
7. 若 Pinecone SDK 方法不兼容，必须给出明确报错与降级建议，不可静默失败。

## 已知约束

- Integrated Embedding 场景下，写入记录必须包含 `chunk_text`。
- Pinecone 为最终一致性，写后立刻查询可能短暂不可见。
- 不同 SDK 版本方法可能不同，本 skill 已做能力探测与兼容分支。

## 目录约定

- 执行脚本：`{baseDir}/tools/pinecone-memory.mjs`
- 安装说明：`{baseDir}/SETUP.md`
- 使用反馈：`{baseDir}/USAGE_FEEDBACK.md`

## 官方参考

- https://docs.openclaw.ai/tools/skills
- https://docs.openclaw.ai/tools/creating-skills
- https://docs.openclaw.ai/tools/clawhub
