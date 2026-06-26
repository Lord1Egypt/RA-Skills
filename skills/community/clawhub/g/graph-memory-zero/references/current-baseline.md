# graph-memory optimized baseline (snapshot: 2026-03-27)

## Runtime placement

- Plugin id: `graph-memory`
- Slot: `plugins.slots.contextEngine = graph-memory`
- Enabled: `plugins.entries.graph-memory.enabled = true`

## Model stack

- LLM:
  - `baseURL = https://api.siliconflow.cn/v1`
  - `model = deepseek-ai/DeepSeek-V3.2`
- Embedding:
  - `baseURL = https://api.siliconflow.cn/v1`
  - `model = Qwen/Qwen3-Embedding-8B`

## Recall policy (balanced profile)

- `scope = all`
- `threshold = 0.62`
- `infer = true`
- `filters.memoryType = all`
- `preferenceLexicon`:
  - `version = 2026-03-27.balance-v1`
  - `enabled = true`
  - `keywords = [preference, prefer, like, default, style, habit, 偏好, 喜欢, 默认, 风格, 习惯, 口味, 倾向]`
  - `notes = Balanced default profile for recall governance`

## mem0-aligned semantics to communicate

- `threshold` is accepted as mem0-style alias of `minScore`
- if both `threshold` and `minScore` are present, strict value wins (`effectiveThreshold = max(...)`)
- `infer` is deterministic query inference (no extra LLM call)
- `memoryType` introduces fact/preference/task/event/all governance while preserving old filters
- `preferenceLexicon` supports runtime hot updates (effective on subsequent recall calls)
- `gm_search.details.debug` exposes effective threshold/infer/filter summary for observability

## Operational notes

- Prefer `gateway.config.patch` over manual config rewrite.
- Keep patches minimal and scoped to `plugins.entries.graph-memory.config`.
- If local tests fail but config intent is clear, use patch+verify flow and keep rollback notes.

## Version note

- `openclaw.plugin.json` / `package.json` currently show `1.5.7` in extension folder.
- `plugins.installs.graph-memory.version` in runtime config shows `1.5.6`.
- Treat this as a metadata mismatch check item before external release.
