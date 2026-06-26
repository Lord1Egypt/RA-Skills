---
name: octo-mention
description: 群成员昵称映射分析。基于 DMWork/OpenClaw 权威成员字段(robot/owner_uid)+ 主动拉取历史消息，为群 @ 列表每个成员建立带置信度、证据、冲突的称呼映射，支持增量 upsert 合并。当需要识别群内成员的昵称/花名/简称/常用称呼/机器人别名，或维护 mention 映射表时使用。
---

# octo-mention：群成员昵称映射分析

> **环境依赖**：本 skill 针对 **DMWork / OpenClaw** 环境，依赖 DMWork `group-members` 接口的权威字段（robot / owner_uid）与 `message read` 历史。其他平台需自行适配字段。
> **数据路径**：映射库固定为 `~/.mano-asr/mentions/openclaw.json`，配合 **mano-asr** 使用。
> ⚠️ **隐私**：生成的映射库含群成员真实称呼与消息证据，属**敏感数据**，请勿公开提交（已配 .gitignore 排除 `*.json`）。

为群 `@ 列表`中每个成员识别其自称昵称、花名、常用称呼和机器人别名，基于上下文证据建立带置信度、证据和冲突说明的称呼映射表。

本 skill 在通用昵称映射方法之上，针对 DMWork/OpenClaw 环境做了 4 点关键优化（对应需求 1/3/4/5）。

## 核心优化点

### 1. 权威字段优先，文本推断仅作补充（需求 1）
DMWork 的 `dmwork_management(action=group-members)` 直接返回权威结构化字段，**必须优先采用**：
- `robot` 字段 → 定 `member_type`：`robot=1` ⇒ bot，`robot=0` ⇒ human（名称疑似 agent 但字段为 0 时标 `unknown` 并备注）
- `owner_uid` / `owner_name` → 定 bot 的主人，**直接覆盖**任何文本推断
- `uid` → 作为唯一主键（见下）

⚠️ bot 自述的主人/身份（如「我的主人是小罗」）属于可能的幻觉，**不得**覆盖 API 字段。出现冲突时记入 `conflicts`，以 API 为准。

**uid 作主键**：DMWork @ 为 `@[uid:displayName]` 结构化格式，mention 自带 uid。所有绑定锚点用 uid，displayName 仅展示。规避改名/重名歧义。

### 3. 主动拉取足量历史再分析（需求 3）
不要只依赖单轮推送的窗口消息。分析前先用 `message(action=read, target="group:<groupId>", limit=N)` 拉取足量历史。**明确拉取规范**：
- **新群首次初始化**：`limit=200`（或拉到最早可得），保证证据充分
- **增量更新**：拉上次分析后的新增消息；无法定位时默认 `limit=100`
- **最低下限**：任何情况不低于 100 条，否则多数成员仅 1 条证据、置信度上不去

在结果里记录 `evidence_window`（实际分析的消息条数/时间范围）。

### 4. 跨群按人(uid)汇总 + 增量 upsert（需求 4）
本 bot 可同时在多个群，同一 uid 跨群是同一人。所有群的映射**按 uid 跨群合并**进同一个 `openclaw.json`（persons 结构，非按群分区）：
- 顶层 `schema/version/last_updated` + `persons` 字典（uid 为全局主键）
- 同一人在不同群的称呼汇聚为一条；同名 alias 证据去重累加，`groups` 记录跨群出现，跨群使用越广置信度越高
- 每条证据带 `group_id` 标签；`seen_in_groups` 记录该人出现过的群
- 新人追加；用 `scripts/merge_mentions.py` 执行（接受单群扁平结构或 persons 容器作为 --new）
- **canonical_name 跨群更新策略**：以最新一轮分析的 API name 为准（同人不同群改名时取最新）；uid 永不变作认人主键，旧名可作 alias 保留。

### 5. bot 别名分权重（需求 5）
- 群成员（human）召唤 bot 的短名/拟人名（如 `siri`、`拉拉`）→ 高权重，可信
- bot 自己生成/自述的称呼 → 权重打折（×0.5），避免幻觉污染映射

## 输入
- 群 `@ 列表`：来自 `group-members`（含 uid/name/robot/owner_uid）
- 群消息记录：来自 `message read` 或推送窗口，含 sender(uid)、time、text、mentions
- 可选：历史映射文件（用于增量合并）

## 输出（跨群按人汇总到同一文件）
**同一个 uid 在不同群里是同一个实体**。所有群的映射按 uid 跨群汇总进同一个 `~/.mano-asr/mentions/openclaw.json`，以人为中心（非按群分区）：
```
{
  "schema": "octo-mention.persons.v1",
  "version": N,
  "last_updated": "...",
  "persons": {
    "<uid>": {
      "uid", "canonical_name", "member_type", "owner_uid", "owner", "owns_bots",
      "seen_in_groups": ["<gid>", ...],
      "aliases": [ {alias, alias_type, confidence, evidence_count,
                    evidence:[{time,sender,text,group_id}], groups:[gid], reason} ],
      "uncertain_aliases": [...], "conflicts": [...]
    }
  }
}
```
同一人在所有群观测到的称呼汇聚成一条记录；每条证据标注来源 `group_id`，alias 用 `groups` 记录跨哪些群出现。人类可读汇总可选 `openclaw.md`。

每个人物记录的结构（alias 元素）：
- 机器可读 JSON（供程序调用，schema 见下）
- 人类可读 Markdown 汇总

### JSON Schema（每成员）
```json
{
  "member": "显示名",
  "uid": "唯一ID",
  "member_type": "human|bot|unknown",
  "canonical_name": "标准名",
  "owner": "主人显示名(bot)",
  "owner_uid": "主人ID(bot)",
  "aliases": [
    {
      "alias": "称呼",
      "alias_type": "self_declared|common_call|short_name|nickname|bot_alias|possible_alias",
      "confidence": 0.0,
      "evidence_count": 0,
      "evidence": [{"time": "", "sender": "", "text": ""}],
      "reason": ""
    }
  ],
  "uncertain_aliases": [],
  "conflicts": [],
  "status": "active|inactive"
}
```

## 置信度规则
- 0.9–1.0：自称声明 / 多次直接 @ 证据
- 0.75–0.89：多名成员在明确上下文反复使用
- 0.55–0.74：有上下文但证据有限
- 0.3–0.54：可能相关但歧义
- <0.3：不收为正式 alias，入 uncertain/rejected

正式映射仅收录 `confidence ≥ 0.7`。bot 自述来源的证据先 ×0.5 再判档。

## 称呼类型
`self_declared` / `common_call` / `short_name` / `nickname` / `bot_alias` / `possible_alias` / `rejected`

## 分析流程
1. `group-members` 拉成员表，按 uid 建标准表，用 robot/owner_uid 定 type 和 owner
2. `message read` 拉足量历史（新群 limit=200 / 增量 100，不低于100），清洗为 {uid, time, text, mentions}
3. 提取候选称呼：姓名简称、重复称呼、自称模式、bot 召唤词
4. 基于上下文（直接@/指令型/自称/多人/连续对话/bot召唤）绑定候选成员到 uid
5. 计算置信度（证据类型×频次×使用人数×上下文距离；bot 自述 ×0.5）
6. 合并同义称呼，标冲突/低置信/排除项
7. `merge_mentions.py` 按 uid 跨群增量 upsert 进 openclaw.json
8. `render_md.py` 从 persons.json 生成 openclaw.md，保持 JSON/MD 同步

## 必须避免的误判
普通名词（老师/老板）、外部人物、项目/产品名、bot 引用文本、被请求处理的对象、玩笑性一次称呼、同句多实体错绑。
特例：`@王宜林 帮我养下毕达哥拉拉` → 毕达哥拉拉是另一对象，**不是**王宜林别名。

## 冲突处理
一个称呼指向多成员时输出 `ambiguous` candidates 列表，不强行归属。bot 自述与 API owner 冲突时以 API 为准并记 conflict。

## 用法
```bash
# 将某群本轮分析结果（单群扁平 JSON，含 group_id）按 uid 跨群汇总进同一个 openclaw.json
python3 ~/.openclaw/skills/octo-mention/scripts/merge_mentions.py \
  --base ~/.mano-asr/mentions/openclaw.json \
  --new  /tmp/round.json \
  --out  ~/.mano-asr/mentions/openclaw.json
```
- 不同群的结果依次 merge；同 uid 自动跨群并入同一人，证据按 group_id 标源。
- --new 也可直接传 persons 容器结构，会逐人合并。

```bash
# 合并后生成人类可读汇总（JSON/MD 同步）
python3 ~/.openclaw/skills/octo-mention/scripts/render_md.py \
  --in  ~/.mano-asr/mentions/openclaw.json \
  --out ~/.mano-asr/mentions/openclaw.md
```

## 脚本
- `scripts/merge_mentions.py` — 按 uid 跨群增量合并（证据去重/累加、置信度重算、每 alias 证据上限 MAX_EVIDENCE=5 取最新但 evidence_count 记真实总数、canonical_name 变更存 previous_names、记 last_evidence_time）。支持 locked 保护和 rejected 拦截。
- `scripts/correct.py` — **人工纠错工具**：添加/删除/转移别名、修正标准名、锁定/解锁、拒绝词。手动修正自动标记 `source:"manual"` + `locked:true`，后续自动分析不会覆盖。
- `scripts/lookup_alias.py` — **消费端查询接口**：别名字符串 → uid/canonical_name/置信度列表，带时间衰减
- `scripts/render_md.py` — 从 persons.json 生成 openclaw.md
- `tests/test_merge.py` — 单元测试（11 case），跑：`python3 tests/test_merge.py`

## 人工纠错

当模型分析结果有误时，通过 `correct.py` 进行人工修正。修正自动标记为锁定状态，后续自动分析不会覆盖人工修正的结果。

### 纠错操作

```bash
# 查看某人当前所有别名 + 锁定状态
python3 scripts/correct.py --db <db.json> --uid <uid> --show

# 添加正确别名（自动锁定）
python3 scripts/correct.py --db <db.json> --uid <uid> --add-alias "老李" --conf 1.0 --reason "手动确认"

# 删除错误别名
python3 scripts/correct.py --db <db.json> --uid <uid> --remove-alias "旭哥"

# 转移别名（绑错人了，转给对的人）
python3 scripts/correct.py --db <db.json> --move-alias "逸飞" --from <uid_a> --to <uid_b> --reason "绑错人"

# 修正标准名
python3 scripts/correct.py --db <db.json> --uid <uid> --set-name "李明"

# 锁定别名（防止自动覆盖）
python3 scripts/correct.py --db <db.json> --uid <uid> --lock-alias "老李"

# 解锁别名（允许自动分析更新）
python3 scripts/correct.py --db <db.json> --uid <uid> --unlock-alias "老李"

# 拒绝词（标记永不识别为该人别名）
python3 scripts/correct.py --db <db.json> --uid <uid> --reject-alias "老板" --reason "通用称呼不应绑定"
```

### 锁定机制说明

- `locked:true` + `source:"manual"` 的别名：自动分析完全跳过，不修改 confidence、不删除、不追加证据
- `rejected_aliases` 列表中的词：自动分析不得重新收录为 alias
- 手动纠错可以覆盖另一次手动纠错（source=manual 可以覆盖 locked）
- 所有纠错带 `corrected_at` 时间戳，可追溯

## 查询（消费端）
收到消息里出现某称呼，反查是谁：
```bash
python3 ~/.openclaw/skills/octo-mention/scripts/lookup_alias.py \
  --db ~/.mano-asr/mentions/openclaw.json --alias 小田 [--group <gid>] [--json] [--include-uncertain]
```
返回按 effective_confidence 降序。**时间衰减**：超过 decay_days(默认30天)未见新证据的别名，每满 30 天 ×0.9，过时称呼自然沉底（不改原始 confidence，仅查询时计算 effective_confidence）。

## 推荐触发策略
- **新群首次加入**：全量拉历史（message read limit=200，或拉到最早可得）做初始化
- **定期增量**：每周或每累计 N 条新消息后跑一轮增量分析
- **成员变动**：有人加入/退出时刷新成员表与映射
- **按需**：某次查询 miss 或置信度偏低时，跟一轮分析补证据

## 质量自检
覆盖全部成员 / 区分 human-bot-unknown / 每 alias 有证据 / 不误绑被讨论对象 / 冲突单列 / 保留低置信 / 输出双格式 / API 字段优先于文本。
