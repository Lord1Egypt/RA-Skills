---
name: "memory-tuner"
description: "按读取频率追踪并优化 MEMORY.md 长期记忆：埋点、冷热统计、降级/上移/清理。"
metadata:
  openclaw:
    requires:
      bins: ["python3"]        # 加载时自动检查宿主有没有这个命令
    emoji: "🧠"
    homepage: "https://clawhub.ai/smliences/skills/memory-tuner"
---

# memory-tuner — 长期记忆按读取频率调优

## 解决的问题

MEMORY.md 只增不减会无限膨胀。OpenClaw 没有"多久没被读到就自动删"的机制（无 LRU/TTL；dreaming 只做晋升不做淘汰；且无 memory 工具级 hook 可挂）。本 skill 用**自律埋点 + 定期统计 + 分级处置 + 容量淘汰**实现按读取频率优化：

- 热条目 → 上移到 MEMORY.md 更靠前的位置（引导注意）
- 冷条目 → 降级到 memory/archive/（内容保留，退出长远注入）
- 冻结条目 → 清理（先备份到 ~/.Trash）
- 常青条目（含 `<!-- keep -->`）→ 永不降级
- **超水位条目**（Redis allkeys 式）→ 按 lru/lfu 策略淘汰候选，降到水位以下

## 触发时机

1. **埋点（每次会话顺手做）**：当我在对话中实际用到了 MEMORY.md（或 memory/*.md）某条目的内容——无论是通过 `memory_search`/`memory_get` 命中，还是 bootstrap 注入后我在回复中直接引用了它——按下面规则追加一条读取记录。
2. **统计与处置（定期维护）**：由 automation 每周触发一次（建议周一 10:00，`agentTurn` 提示词引用本 skill）；也可在用户要求"优化记忆"时手动执行。

> ⚠️ 不可把"bootstrap 全文注入"当作读取：MEMORY.md 每次会话都会整文件注入，无法区分条目，统计它没有意义。只统计**主动检索命中**与**实际引用**。

## 埋点规则（agent 行为，非脚本）

- 追踪目录：`memory/.track/`（如不存在则创建）
- 文件：按月 `memory/.track/YYYY-MM.md`，每行一条：
  ```
  YYYY-MM-DD | <条目key> | search|get|use
  ```
  - `search` = memory_search 命中该条目所在文件/主题
  - `get` = memory_get 读取了所在行区间
  - `use` = 回复中实际引用了该条目内容（最可靠信号，权重最高）
- **自动与手动分工**：`search`/`get` 两类埋点由配套插件 **memory-tuner-observer**（ClawHub 包 `smliences/memory-tuner-observer`，after_tool_call hook 拦截 memory_search/memory_get）**自动记录**，无需人工；`use` 仍由本 skill 规则手动记（插件无法判断模型是否真的引用了结果）。
- **计数口径（v2 简化）**：每实际引用一次就追加一行，**不做同日/同会话去重**；行数 = 被引用次数。埋点零成本：无需 grep 查重，直接 append 即可（同会话内反复引用同一条就记多行，频次正是热度信号）。
- **条目 key 的取法**：优先用 MEMORY.md 中的条目标题（`## ` 节名）或 bullet 加粗名（`- **xxx**`）；拿不准就用节名。命中多条就各记一行。
- 跳过：`memory/archive/` 里的内容不埋点（已降级，不再追踪）。

## 统计脚本

自带 `scripts/memory-tuner.py`（只读分析，不改文件）：

```bash
python3 scripts/memory-tuner.py                      # 默认：分析 + 出报告（dry-run，lfu 策略）
python3 scripts/memory-tuner.py --policy lru         # 淘汰候选按 lru（最久未读）排序
python3 scripts/memory-tuner.py --policy lfu         # 淘汰候选按 lfu（引用最少）排序（默认）
python3 scripts/memory-tuner.py --mark               # 额外在冷/冻条目上加 <!-- cold --> / <!-- frozen --> 注释
python3 scripts/memory-tuner.py --json               # 机器可读输出
```

脚本支持 `OPENCLAW_WORKSPACE` 环境变量覆盖工作区根目录（默认 `~/.openclaw/workspace`），便于多机/多用户使用。

### 统计口径

- 解析 MEMORY.md：`## ` 为节，节内 `- **加粗标题**`（或 `- ` bullet）为条目；尊重 `<!-- keep -->`（常青）、`<!-- cold: 日期 -->`、`<!-- frozen: 日期 -->` 标注。
- 输入 `memory/.track/*.md` 的行，按 key 模糊匹配（节名/加粗名包含匹配）。行数即引用次数，直接累计。
- 指标：`hits`（总引用次数）、`hits_30d`（30 天内引用次数）、`hits_90d`（90 天内引用次数）、`last_hit`（最后引用日期）、`sources`。
- 分级（阈值可调，见脚本头常量）：
  | 档位 | 条件 | 建议动作 |
  |------|------|---------|
  | hot | hits_30d ≥ 1 | 上移到本 section 顶部 |
  | warm | 有引用记录但 30d 内无 | 保留不动 |
  | cold | last_hit > 30d 且 hits_90d = 0，无 keep | 降级到 memory/archive/ |
  | frozen | last_hit > 60d 且 hits_90d = 0，无 keep | 备份后清理（或合并进更概括条目） |
  | untracked | 无任何引用记录 | 人工复核（区分刚写入 vs 过时内容），不自动处置 |
  - 命中 `use` 记 2 分、`search`/`get` 记 1 分参与排序（简单加权，不搞复杂模型）。
  - 新条目（写入 < 14 天）不判冷，有冷却期——埋点数据不足时以 untracked 呈现，靠处置流程人工复核兜底。
- **容量水位（Redis allkeys 式淘汰）**：
  - 常量 `MAX_ITEMS = 30`（条目数上限）、`MAX_BYTES = 8KB`（体积上限），见脚本头，可调。
  - 超**条目水位** → 按 policy 生成淘汰候选清单：优先淘汰 frozen→cold→warm→untracked，同档内按 lru（last_hit 最久远）或 lfu（score 最低，平局看 last_hit 更旧）排序；`<!-- keep -->` 与 hot 永不进入候选。
  - 只超**字节水位**（条目数未超）→ 提示精简长条目或调高 MAX_BYTES，不自动淘汰（字节超多是长条目问题，删条目未必够）。

### 输出

Markdown 报告：各条目热度表 + 各自建议动作 + 容量水位检查；结尾给一个"本次建议执行清单"（哪些上移、哪些归档、哪些清理、哪些是超水位淘汰候选）。

## 处置流程（agent 执行，脚本不直接动文件）

1. 先跑 `--mark` 出报告，**给用户过目**（默认模式）；untracked 条目人工扫一遍：明显刚写入/仍相关 → 不动；明显过时 → 按 cold 流程走。用户确认（或 automation 已授权自动档）后再执行。
2. **上移**：把 hot 条目移到所属 section 的最前面（section 顺序和条目前后都代表优先级）。
3. **降级**：cold 条目（及用户确认的超水位淘汰候选）从 MEMORY.md 删除，整段追加到 `memory/archive/MEMORY-<YYYY-MM>.md`（保留原文与来源日期），并在当日日记记一笔。
4. **清理**：frozen 且非 keep 的，先在 MEMORY.md 里确认无引用价值 → 备份到 ~/.Trash 后删除（不要直接 rm）。
5. 处置完更新追踪文件（归档动作本身记一行 `use`，日期=处置日），并把 `<!-- cold -->` 之类的标注清掉。
6. 若置为全自动档：仍保留"每个 key 动作一行"的变更摘要回报用户。

## 与现有机制的关系

- 不动 dreaming（未启用；它只管晋升，不管淘汰）。
- 不动 memory_search 索引：归档文件仍在 memory/ 下可被检索；只有清理（删除）会真正移出索引，所以清理前必须备份。
- 与 MEMORY.md 维护原则一致：条目被蒸馏吸收后即可移除，不留"已完成待办"残骸。
- 与 Redis 淘汰的区别：Redis 淘汰是真删，本 skill 的"淘汰"= 降级归档，可恢复——因此可以放心采用 allkeys 语义。

## 边界与保护

- `<!-- keep -->` 一票否决：不判冷不判冻、不进入淘汰候选（例：myblog 触发词、~/software 布局、安全约定）。
- 含密钥/敏感内容的条目即使冷也只降级不清理（降级文件仍在本地）。
- 不处理 memory/*.md 日记正文（那是原始日志层，本 skill 只管长期记忆层）。
- 用户未提交的工作区变更、用户明确说保留的内容，一律不动。

## 配套任务（可选）

用户批准后建一条 cron（建议 `every` 每周一 10:00，或 `cron 0 10 * * 1` Asia/Shanghai），isolated agentTurn 提示词：`运行 memory-tuner skill 的统计与处置流程（dry-run 报告模式，先不执行）`，产出后 announce 给用户决定是否执行。

## 文件清单

- SKILL.md（本文件）
- scripts/memory-tuner.py — 统计脚本（只读 + --mark 标注）
- 使用后生成：memory/.track/YYYY-MM.md、memory/archive/MEMORY-YYYY-MM.md、维护报告（直接并入当日日记即可）
