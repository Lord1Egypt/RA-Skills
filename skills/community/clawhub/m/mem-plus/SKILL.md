# mem-plus v5 — 第一性原则精确召回

基于 **mem-plus**（22k⭐ · Benchmark 最高分）融合 SuperMem 增强层。

---

## 核心理念（第一性原则）

**问题本质**：当城问我任何问题时，我需要准确知道他的身份、偏好、原则、进行中的项目。
**核心需求**：**确定性精确召回** >> 多样性探索

vs 传统 RAG 系统：需要多样性（搜索引擎场景）→ MMR 默认开启
我们的场景：个人 AI 助手 → **精确召回优先**，MMR 可选

---

## v5 架构（vs v4 的本质区别）

```
用户消息
  ↓
message:preprocessed (hook.ts)
  ↓
mem-plus_cli.py search
  ↓
mempalace 底层检索（15条原始结果）
  ↓
strip_metadata() — 清除 OpenClaw 元数据
  ↓
filter_credentials() — 凭证过滤
  ↓
dedup_results() — 同源去重 + Levenshtein
  ↓
identity_kw_boost() ← v5 新增
  • identity_boost: USER.md(+100), SOUL.md(+50), MEMORY.md(+30), AGENTS.md(+10)
  • keyword_boost: 中文bigram精确匹配（解决中文嵌入质量问题）
  ↓
最终排序（原生分数 + boosts，不打乱）
  ↓
可选: mmr_rerank() — 默认关闭
  ↓
注入 bodyForAgent
```

---

## 第一性原则设计决策

| 决策 | v4 | v5 | 原因 |
|------|----|----|------|
| MMR | 默认开启 | 默认关闭 | 个人助手需要确定性，不是RAG |
| 身份优先 | 无 | USER.md +100分 | 城的信息必须随时可用 |
| 中文语义 | 纯向量 | 向量 + Bigram boost | nomic-embed-text 中文质量有限 |
| 凭证存储 | 被动过滤 | 前置检测 + 过滤 + 警告 | fail-secure |

---

## CLI 命令

```bash
# 精确召回（默认，关闭MMR）
mem-plus_cli.py search "城的身份 CEO"

# 开启MMR多样性模式（显式）
mem-plus_cli.py search "城的身份 CEO" --use-mmr

# 存储记忆（含凭证检测）
mem-plus_cli.py remember "城总今天有新任务"

# 检查状态
mem-plus_cli.py status

# 唤醒上下文
mem-plus_cli.py wake-up

# 挖掘新记忆
mem-plus_cli.py mine --path ~/.openclaw/workspace
```

---

## 增强层功能

| 功能 | 状态 | 说明 |
|------|------|------|
| Hook 自动召回 | ✅ v4修复 | message:preprocessed 触发 |
| 解析函数 | ✅ v4修复 | 正确分割 [N] 结果 |
| 同源去重 | ✅ | SKILL.md 不再重复 |
| identity 优先注入 | ✅ v5新增 | USER.md 永远第一 |
| 中文 Bigram boost | ✅ v5新增 | 解决中文嵌入差问题 |
| MMR 多样性 | ✅ 可选 | `--use-mmr` 显式开启 |
| 凭证过滤 | ✅ | ghp_ / mars*** → 占位符 |
| 存储前凭证检测 | ✅ v5新增 | fail-secure |
| 元数据剥离 | ✅ | [message_id:] 等完全清除 |
| ChromaDB forget | ✅ | 删除特定记忆 |

---

## 核心文件

| 文件 | 作用 |
|------|------|
| `scripts/mem-plus_cli.py` | v5 召回引擎入口（19KB） |
| `scripts/mem-plus_reranker.py` | MMR + Levenshtein 去重 |
| `scripts/super_mem_cli.py` | SuperMem bridge（独立层） |

---

## 数据存储

- **mem-plus 原生**：`~/.mempalace/palace/`（387 drawers）
- **SuperMem ChromaDB**：`~/.super-mem/chroma/`（可选层）

---

## 安装要求

- Python 3.9+
- Node.js
- mem-plus CLI：`/Users/mars/Library/Python/3.9/bin/mempalace`
- Ollama：`nomic-embed-text` 模型

---

## 更新日志

### v5 (2026-04-08) — 第一性原则重构
- **FEAT**: identity_boost — USER.md(+100), SOUL.md(+50) 永远优先
- **FEAT**: keyword_boost — 中文 Bigram 精确匹配解决中文嵌入差问题
- **FEAT**: MMR 默认关闭 — 精确召回优先
- **FEAT**: remember 前置凭证检测 — fail-secure
- **FIX**: credential filter 增强 — mars\d{5,} → [PASSWORD]

### v4 (2026-04-08) — 召回链路修复
- **FIX**: hook.ts → 正确 CLI（移除无效参数）
- **FIX**: parse_search_output → 正确分割 [N] 结果
- **FIX**: 同源去重 → SKILL.md 不再出现多次

### v3 及之前
- 早期混合架构（已废弃）
