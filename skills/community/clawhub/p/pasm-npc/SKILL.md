---
name: pasm-npc
description: >-
  Game NPC agents built on the PASM cognitive engine. NpcAgent gives you an NPC with persistent memory
  (salience-aware eviction so landmark events are never pushed out by trivia), persona-weighted action
  selection (temper/energy/play drive the baseline), and feedback-driven shaping - praise or scold a
  SPECIFIC action and the behaviour distribution actually moves. Emotion modulates replies. Growth
  stages unlock new actions (wave/hop/peek -> ball -> dance/spin -> think). Zero LLM dependency,
  offline-runnable, state persists to ~/.pasm-agents/<id>/. Tier label (light/core/bionic) exposed on
  every agent so callers always know which engine path is live.
version: 0.5.0
license: MIT-0
author: arronzheng
homepage: https://github.com/arronJack/pasm-agents
metadata:
  openclaw:
    category: agents
    tags: [ai-agents, pasm, npc, game, memory, emotion]
    requires:
      bins: [python3, git]
      env: []
---

# PASM 游戏 NPC 智能体（pasm-npc）

给游戏装一个**有记忆、有情绪、会被玩家反馈塑形**的 NPC。
零 LLM 依赖、断网可用、状态可持久化 —— 不是写死的台词表，是真的能记住玩家。

```python
from pasm_agents import NpcAgent

npc = NpcAgent(agent_id="herbalist", persona={
    "name": "陈伯", "role": "河边摆摊的草药老头",
    "temper": 0.55, "energy": 0.40, "play": 0.30,
    "tone": "慢悠悠、爱讲道理",
})
npc.observe("玩家第一次来买跌打药", tags=["玩家", "买药"], salience=4, category="日常")
print(npc.act())                 # 'talk' / 'wave' / 'peek' / ...
print(npc.chat("有跌打药吗"))     # 召回相关记忆
print(npc.mood)                  # 情绪值（注意：是属性，不加括号）
npc.feedback("praise", action="talk")   # 显式夸"talk"这个动作
npc.save()                       # ~/.pasm-agents/herbalist/
```

## 这个技能给你什么

| 能力 | 说明 |
|---|---|
| **记忆** | 玩家做过的事逐条入库；重要度 `salience` 分 1/3/5，容量触顶时按「重要度 + 新旧」淘汰 —— 里程碑（"玩家救了我一命"）不会被日常琐事挤掉 |
| **情绪** | 有随事件变化的情绪值；同一句话在高兴和生气时说出来的不一样 |
| **动作** | 从动作池里选动作执行，动作池随成长阶段解锁；被夸的动作做得多，被凶的做得少 |
| **持久化** | 落盘到 `~/.pasm-agents/<agent_id>/`，跨进程自动恢复上次状态 |

**你主要就用这五个方法**：`observe()` 记一件事 · `chat()` 说 · `act()` 做 · `feedback()` 塑形 · `save()` 存。

## 它跑在什么之上：基座 `pasm-skills` + 应用框架 `pasm-framework`

本技能的内容在 **`pasm-agents`** 仓，它**依赖两层**：
`BaseAgent`（记忆读写 / 情绪 / 动作选择 / 反馈 / 持久化的通用实现）在**基座**里，
产品智能体只是在其上定了 persona、动作池和回复模板；
**应用框架**则提供"把智能体接成完整应用 / 服务"的那一层（插件子系统、HTTP 网关、流式输出）。

| | 是什么 | 装它 |
|---|---|---|
| **pasm-skills**（基座） | 只提供能力，**不含任何智能体** | `pip install pasm-skills` |
| **pasm-framework**（应用框架） | 应用级表面：插件子系统 / HTTP 网关 / 流式输出 | `pip install pasm-framework` |
| **pasm-agents**（本技能来源） | 游戏 NPC / 老人陪伴 / 学习陪伴 + 7 个验证智能体 | `pip install pasm-agents` |

> 装 `pasm-agents` 会**自动带上基座与框架**，一条命令搞定 ——
> 用本技能里的智能体**不需要**你直接接触框架层。
> 只装基座时 `python -m pasm_skills list` 显示 0 个智能体 —— 那是刻意的，不是你装错了。
> 想用基座写自己的智能体：<https://github.com/arronJack/pasm-skills/blob/master/docs/TUTORIAL.md>
> 想做**带 HTTP 接口 / 智能客服 / 站点嵌入的应用**：见 `pasm-framework` 仓的 `docs/tutorials/`。

## 什么时候用

- 游戏里需要 NPC **记住玩家做过什么**（救过我 / 抢过我 / 常来买什么），而不是每句台词靠状态机硬编码；
- 希望 NPC **有情绪**，同一句话在高兴和生气时说出来的不一样；
- 希望 NPC 的**行为偏好能被玩家长期塑形**（夸它 → 多做；凶它 → 少做），而不是永远一套权重；
- 想给现有游戏**后接一层认知内核**，但不想自己搭记忆淘汰 / 情绪衰减 / 行为选择。

## 0. 铁律

1. **零 LLM 依赖**：聊天是纯模板 + 记忆检索 + 情绪渲染，不调用任何外部大模型；断网、无显卡、无 API key 都能跑。
2. **PASM 核心真接入**：能用 `pasm.cognitive.memory_layers` / `learning` / `pasm.modules.emotion` 时优先用；
   找不到核心时降级到内置轻量适配，并在 `tier` 字段写明档位，**永不隐藏降级**。
3. **重要度参与淘汰**：`observe(..., salience=1..5)`。容量触顶时按「重要度 + 新旧」淘汰，
   `salience=5` 的里程碑记忆（"玩家救了我一命"）不会被日常琐事挤掉。
4. **反馈必须能指定动作**：`feedback(kind, action=)`。不指定就只能加强"当前最偏好的动作"，
   长期下来行为分布会被推到极端 —— 这是 `npc-lifelong` 验证智能体压出的产品级要求。
5. **持久化开箱即用**：落盘到 `~/.pasm-agents/<agent_id>/`，跨进程加载自动恢复上次状态。
6. **触发词要"专指"，别用宽词**：
   - 问身份只认「你叫什么 / 你是谁 / 你的名字 / 怎么称呼」这类**明确问句**，
     **不放光杆「名字」** —— 否则「我名字叫张三 / 这花有名字吗 / 我给你起个名字吧」
     全会被当成在问 NPC 是谁（2026-09-15 探针实测 4/4 误触发）；
   - **自称由 persona 决定**（`self_ref`，留空用中性「我」），
     别在模板里写死「老朽」—— 否则「卖花的小姑娘」也会说"老朽还记着呢"。

   回归护栏：`python -m pasm_agents.selftest_npc`（12 项，秒级，退出码 0/1）。
   **改触发词或回复模板就顺手跑它** —— 这条通路坏了，别的测试不会报错。

## 1. 30 秒上手

```bash
pip install pasm-agents                    # 自动带上基座 pasm-skills（推荐）
# 没有 PyPI 环境时改源码安装：
#   git clone https://gitee.com/arronzheng/pasm-agents && cd pasm-agents && pip install -e .

pasm-agents demo npc                      # 预置剧本，立刻看到效果
pasm-agents run npc --id=my_herbalist     # 交互模式
pasm-agents inspect my_herbalist          # 看落盘快照（记忆 / 情绪 / 权重）
```

## 2. 人格怎么定

`persona` 里三个性格量决定动作基线（0~1）：

| 字段 | 含义 | 高 → 偏向 | 低 → 偏向 |
|---|---|---|---|
| `temper` | 脾气 | 主动搭话、反应大 | 沉默、旁观 |
| `energy` | 精力 | 走动、干活 | 休息、打盹 |
| `play`   | 玩心 | 蹦跳、逗趣 | 正经、务实 |

再加 `tone`（语气描述，写进回复模板）与 `role`（身份，用于自我介绍）。
`self_ref`（可选）是 **NPC 的自称**：留空用中性「我」，老派角色可写「老夫」「老朽」。
它**必须由 persona 给** —— 别指望模板默认值，写死就会出现
「卖花的小姑娘说：老朽还记着呢」这种**人设泄漏**。

## 3. 记忆怎么用

```python
# 日常记忆（默认 salience=1，容量触顶时先被淘汰）
npc.observe("玩家买了三副跌打药")

# 里程碑记忆（重要度 5，永远不会被挤掉）
npc.observe("玩家在河边把我从水里拉了上来",
            brief="我差点淹死", tags=["玩家", "河边", "救命"],
            salience=5, category="重大")

# 检索：chat 内部会自动召回；也可以手动拿
print(npc.recall("河边", k=3))       # -> [{'title': ..., 'brief': ..., ...}, ...]
print(npc.chat("还记得上次在河边吗"))
```

`observe` 完整签名：

```python
observe(title, brief="", tags=None, *, salience=1, category="日常")
```

`salience` 语义：`1` 日常 / `3` 值得记 / `5` 里程碑。

## 4. 情绪与动作

```python
print(npc.act())          # 选一个动作执行
print(npc.mood)           # 当前情绪（**属性**，不是方法）
npc.feel("被玩家救起", valence=+0.8)     # 手动注入一次情绪事件（-1 ~ +1）
npc.feedback("praise", action="talk")    # 被夸 → talk 权重上升
npc.feedback("scold",  action="hop")     # 被凶 → hop 权重下降
```

**动作池随成长阶段解锁**：

| 阶段 | 动作 |
|---|---|
| 0（初始） | `wave` `hop` `peek` `talk` |
| 1 | + `ball` |
| 2 | + `dance` `spin` |
| 3 | + `think` |

```python
print(npc.grow())         # 手动升一档（按交互数也会自动触发）
```

## 5. 交互模式

```bash
pasm-agents run npc --id=my_herbalist --persona-file=personas/herbalist.json
```

进交互后直接打字对话。可用命令：

| 命令 | 作用 |
|---|---|
| `act` | 执行一个动作 |
| `mood` | 看当前情绪 |
| `observe <文本>` | 手动写一条记忆（salience=2） |
| `feedback <praise\|poke\|scold> [动作]` | 给反馈，可指定动作 |
| `grow` | 升一档 |
| `snapshot` | 导出快照（JSON） |
| `quit` | 退出并 save |

## 6. 档位透明

| tier | 含义 | 何时启用 |
|---|---|---|
| `bionic` | 仿生：完整 PASM 核心 + emotion 模块（需 torch） | `pip install pasm-agents[torch]` |
| `core`    | 完整：PASM 核心（memory + learning，无 torch） | `PASM_PYTHON` 指向带核心的 Python |
| `light`   | 轻量：纯内置（重要度淘汰 + 字面检索 + softmax 权重） | 任何机器 |

落盘 JSON 与 `summary()` 都带 `tier` 字段，调用方一眼能判断当前档位。

## 7. 写你自己的 NPC

子类化 `NpcAgent` 覆盖两处即可：

```python
from pasm_agents import NpcAgent

class Guard(NpcAgent):
    def action_pool(self):
        return ["patrol", "salute", "warn", "rest"]

    def _render_reply(self, text, facts, mood):
        # facts 是检索到的记忆，mood 是当前情绪 —— 据此渲染语气
        return "……（自己写）"
```

`_render_reply(text, facts, mood) -> str` 是唯一的渲染钩子，`chat()` 会调它。

## 8. 与验证层的关系

本仓的 `pasm_agents/verifiers/npc_lifelong.py` 是**专门验证这类 NPC 的智能体**：
跑 90 天 / 270 段经历，断言核心能否正确记忆、里程碑会不会被挤掉、情绪会不会漂、行为会不会僵化。

它压出的真问题已经被修进 **基座** `pasm_skills/sdk/base.py` 的 `_CoreAdapter` —— **你用的就是修过的版本**。

要查最新问题清单，看 `docs/AGENTS.md`。

## 9. 相关技能

- `pasm-companion` —— 老人陪伴智能体
- `pasm-tutor` —— 学习陪伴智能体
- `pasm-longterm-verify` —— 验证层入口：回答"跑久了还是好的吗"
