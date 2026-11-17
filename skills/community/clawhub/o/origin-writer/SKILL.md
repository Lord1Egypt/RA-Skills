---
name: origin-writer
description: 百万字小说写作引擎——把长篇写作变成事务性写作。AI 每写一章提交一个语义事务（正文+状态变更），门禁逐条复核（禁区/伏笔状态机/正文对照）后才落盘。角色不会突然用上他不知道的信息，物品不会凭空易主，伏笔不会收了又埋。新会话秒恢复：state 一条命令拿到全部世界状态。当需要写长篇小说、续写长篇、维护小说世界观一致性、管理伏笔/人物状态/时间线时使用。
version: 1.1.1
slug: origin-writer
license: Apache-2.0
displayName: OriginWriter 百万字小说写作引擎
summary: 把长篇写作变成事务性写作：每章一个语义事务，五道门禁复核后落盘，人物/伏笔/世界状态全程可验证。
metadata:
  openclaw:
    runtime: node >= 18
    tags: [writing, novel, story, world-state, consistency]
---

# OriginWriter · 百万字小说写作引擎

长篇小说写不长、写不圆的病根是同一个：**世界状态只存在于模型的上下文里**。
写到第 30 章，模型已经忘了第 3 章埋的伏笔、第 9 章受的伤、谁在什么时候知道了什么。
上下文会丢，状态不会——前提是它被持久化，并且每次改动都过门禁。

OriginWriter 把长篇写作变成**事务性写作**：每写一章 = 提交一个语义事务
（正文 + 状态变更声明），五道门禁全过才落盘，失败零写入并返回可据以重写的理由。

## 安装

```bash
# 本象协议仓库（含引擎、世界规格、自测）：
git clone https://github.com/dongsheng123132/2origin.git
cd 2origin

# 验证引擎可用：
node adapters/story/selftest.mjs        # 42 项自测
```

## 用

```bash
# 1. 从世界规格建写作包（世界重放到第 10 章，之后由你写）
node adapters/story/cli.mjs init <specDir> <pkg.origin> --until 10

# 2. 新会话第一件事：拿世界状态投影（秒恢复）
node adapters/story/cli.mjs state <pkg.origin>

# 3. AI 写一章，以事务提交（正文 + 状态变更）
node adapters/story/cli.mjs submit <pkg.origin> ch11.json

# 4. 伏笔图谱 / 章节登记表 / 事务水位
node adapters/story/cli.mjs hooks <pkg.origin>
node adapters/story/cli.mjs outline <pkg.origin>
node adapters/story/cli.mjs seq <pkg.origin>
```

事务文件（ch11.json）形状：

```json
{
  "chapter": 11,
  "transaction_id": "ch11-s01",
  "text": "…本章正文…",
  "state_changes": [
    { "object": "obj:black-key", "field": "holder", "from": "char:zhao-qi", "to": "char:lin-zheng", "basis": ["scene:11-07"] }
  ],
  "assertions": ["zhao-qi-alive", "gate-not-opened", "betrayal-undisclosed"],
  "hooks": [{ "id": "hook:new-mystery", "summary": "…", "status": "planted_unresolved", "setup": { "chapter": 11 } }]
}
```

## 门禁五道（全过才落盘）

| # | 门禁 | 抓什么 |
|---|---|---|
| ① | 正文非空 | 写作事务交不出正文就是没干活 |
| ② | 结构/引用/快照隔离 | 未知对象、缺字段、记错前值（降级为警告，累计为「模型记忆偏差率」） |
| ③ | 禁区约束 | 世界规格声明的禁区（钥匙不得用、关键角色不得死、主角不得获知某秘密…） |
| ④ | 伏笔状态机 | 伏笔状态非法取值；回收无依据（hook-payoff） |
| ⑤ | 正文对照状态 | 正文写了「左手挥刀」「正午开门」等与状态矛盾的细节（CED 规则扫描） |

另有**模型自报断言复核**：事务里的 `assertions` 是 AI 自己立的字据
（「我保证赵七还活着」「我保证钥匙没用过」），门禁逐条验收。

## 世界规格（spec）约定

```
specDir/
├── canon/*.jsonl              # 初始对象：characters / locations / objects / factions（id 前缀定类型）
├── narrative/foreshadowing.jsonl  # 伏笔：id / summary / setup.chapter / payoff.chapter
├── timeline/state-changes.jsonl   # 重放历史：object / field / from / to / chapter / evidence
└── tasks/*.json               # forbidden_zones（禁区，machine_check 可机器判定）
```

`--until N`：世界重放到第 N 章，之后的变更由作者亲手以事务提交。
重放历史逐条进 provenance，`origin why <pkg> obj.field` 能回答「这个值凭什么」。

## 验证

```bash
node adapters/story/selftest.mjs    # 42 项断言
node adapters/story/demo.mjs        # 完整演示（建包→恢复→提交→禁区拒绝→伏笔图谱）
```

## 相关

- ShadowBench-W：百万字续写基准（benchmark/shadowbench-w/），OriginWriter 是其引擎化产物。
- 本象协议（benxiang-protocol）：AI 时代的持久对象表示层（Origin IR + 语义事务 + 证据链）。
- 同类场景：Shadow Memory（MCP Server，项目状态持久化）——长篇写作是世界状态持久化的
  一个特例，通用项目管理是另一个。

---
