---
name: pasm-tutor
description: >-
  Learning tutor agents built on the PASM cognitive engine. LearningTutor tracks per-topic mastery
  with an EMA (single bad attempt does not crater it), selects the weakest topic next (with 20% jitter
  to avoid grinding one topic), replies in an encouraging template that admits difficulty and offers
  the smallest actionable step, and exports a stable machine-readable snapshot (mastery / weakest /
  average / history_size / tier) for downstream profile engines. Wrong answers are stored as
  salience-3 memories so related mistakes can be recalled. Zero LLM dependency, offline-runnable.
  Keywords: pasm, tutor, mastery, adaptive practice, student profile, offline.
version: 0.5.0
license: MIT-0
author: arronzheng
homepage: https://github.com/arronJack/pasm-agents
metadata:
  openclaw:
    category: agents
    tags: [ai-agents, pasm, tutor, education, mastery, offline]
    requires:
      bins: [python3, git]
      env: []
---

# PASM 学习陪伴智能体（pasm-tutor）

给学生的陪伴式学习助手：**薄弱点定位 + 最弱优先选题 + 鼓励式对话 + 学情可机读导出**。
零 LLM 依赖、断网可用、状态可持久化。

```python
from pasm_agents import LearningTutor

t = LearningTutor(agent_id="xiaoya", persona={
    "name": "小雅", "grade": "五年级",
    "topics": ["分数加减", "面积计算", "行程问题", "鸡兔同笼"],
})

t.report("分数加减", 0.4)      # 报告一次作答得分（0~1）
t.report("分数加减", 0.5)
t.report("面积计算", 0.9)

print(t.pick_next())          # -> '行程问题'（最弱优先）
print(t.mastery("面积计算"))   # -> 0.27
print(t.chat("分数加减好难"))  # 鼓励 + 具体下一步
print(t.chat("我哪里不行"))    # 直接给出最弱项 + 掌握度
print(t.snapshot())           # 学情结构（纯 JSON，画像层可直接消费）
```

## 这个技能给你什么

| 能力 | 说明 |
|---|---|
| **掌握度追踪** | 每个知识点一个 0~1 掌握度，用 EMA 平滑，越近的表现权重越高 |
| **最弱优先选题** | `pick_next()` 有 80% 概率挑最薄弱的知识点，20% 随机防"只刷熟题"的假象 |
| **鼓励式对话** | 按当前掌握度与近期表现渲染语气；说"我不会"和说"我会了"给不同反馈 |
| **学情可机读导出** | `snapshot()` 输出纯 dict（学生 / 各知识点掌握度 / 最弱项 / 平均 / 档位），画像层可直接消费 |

**你主要就用这几个方法**：`report(topic, score)` · `pick_next()` · `chat()` · `mastery(topic)` · `snapshot()` · `save()`。

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

- 需要**按知识点追踪掌握度**，而不是只记总分；
- 需要**自适应选题**：总是推最该练的那个，而不是随机或顺序出题；
- 需要**鼓励式对话**而不是打击式反馈（"这一步你上次也栽了，我们换个讲法"）；
- 需要一份**机器可读的学情快照**，接进自己的画像 / 报表 / 家长端。

## 0. 铁律

1. **掌握度用 EMA 追踪**：`report(topic, score)` 做指数滑动平均
   （`新 = 旧*0.7 + 本次*0.3`），单次失手不会把掌握度打到谷底，连续失误才真正下探。
2. **选题可解释**：`pick_next()` 返回"当前掌握度最低的知识点"，
   同时给出理由 —— 不是黑箱推荐。
3. **回复必须鼓励式**：不说"你怎么又错了"，说"这块确实容易混，我们换个角度"。
4. **零 LLM 依赖**：讲解走模板 + 知识点状态，不调用外部大模型；断网可跑。
5. **学情可导出**：`snapshot()` 输出稳定结构的纯 JSON，
   **上层画像引擎可以直接消费**，不需要解析自然语言、也不需要伸手进内部字典。
6. **触发词要指向题目，宽词一律不收**：
   - 抱怨分支只认「不会 / 搞不懂 / 太难 / 做不出」这类**明确指向题目**的说法，
     不收光杆「难」—— 否则「**我今天很难过**」（情绪）会被答成"先做 3 道分数加减"；
   - "学会了"分支不收「OK」这种**两字母串**，它会命中任何含 OK 的文本；
   - **判定不了就落到默认分支**（无法判定 = 放行），不硬猜。

   回归护栏：`python -m pasm_agents.selftest_tutor`（12 项，秒级，退出码 0/1）。

   > ⚠️ 这个护栏有个**前车之鉴**值得你知道：它原来断言"回复里提到的知识点 == 本次
   > `pick_next()`"，结果偶发失败 —— 因为 `pick_next()` 是带抖动的，而渲染回复时
   > 会**再调一次**，等于对两次独立随机抽样要求相等。
   > **你自己写测试时别这么写**：要确定性的最弱项，用 `snapshot()["weakest"]`。

## 1. 30 秒上手

```bash
pip install pasm-agents                    # 自动带上基座 pasm-skills（推荐）
# 没有 PyPI 环境时改源码安装：
#   git clone https://gitee.com/arronzheng/pasm-agents && cd pasm-agents && pip install -e .

pasm-agents demo tutor                 # 预置剧本（小雅 30 天 × 4 题）
pasm-agents run tutor --id=my_tutor    # 交互模式
pasm-agents inspect my_tutor           # 看落盘快照
```

## 2. persona 里必须有的东西

| 字段 | 必填 | 说明 |
|---|---|---|
| `name` | ✅ | 学生称呼 |
| `grade` | 建议 | 年级，写进回复模板 |
| `topics` | ✅ | 知识点列表。**这张表就是你的课程大纲** |
| `tone` | 建议 | 语气（默认"温柔、耐心"） |

不传 `topics` 时用内置的 6 个五年级知识点：分数加减 / 面积计算 / 行程问题 /
鸡兔同笼 / 质因数分解 / 图形对称。

## 3. 掌握度与选题

```python
print(t.report("行程问题", 0.3))     # -> {'topic': '行程问题', 'new_mastery': 0.09}
print(t.report("行程问题", 0.35))    # -> {'topic': '行程问题', 'new_mastery': 0.168}

print(t.mastery("行程问题"))          # 0.168
print(t.pick_next())                 # '行程问题'（现在最低）
print(t.snapshot())
# {
#   "student": "小雅", "grade": "五年级",
#   "mastery": {"分数加减": 0.12, "面积计算": 0.27, "行程问题": 0.168, ...},
#   "weakest": "图形对称",
#   "average": 0.145,
#   "history_size": 3,
#   "tier": "light"
# }
```

> `pick_next()` 有 **20% 的抖动**：80% 概率给最弱项，20% 随机选一个防"刷同一个知识点"。
> 要严格确定性的选题，直接用 `snapshot()["weakest"]`。

**推荐阈值**（由调用方决定，本技能只提供数值与排序）：
掌握度 < 0.5 视为薄弱，0.5~0.8 巩固，> 0.8 可推进新内容。

## 4. 对话

```python
print(t.chat("分数加减好难"))     # 共情 + 具体下一步（不是空洞鼓励）
print(t.chat("我哪里不行"))       # 直接列最弱项 + 掌握度数字
print(t.chat("我会了"))           # 鼓励 + 推两道巩固
```

回复模板走的是"**承认难度 + 给最小可行动作**"，避免"加油你可以的"这类无效安慰。
渲染集中在 `_render_reply(text, facts, mood)`，子类可覆盖。

## 5. 用错题记忆做横向关联

每次 `report` 会顺带写一条记忆：得分 < 0.6 记 `salience=3` + `category="错题"`，
否则 `salience=2` + `category="进步"`。所以它能做"这道题和上次那道错的是一类"：

```python
t.observe("上次在'相遇问题'上把速度和当成路程了",
          tags=["错题", "行程问题"], salience=3, category="错题")
print(t.chat("行程问题又不会了"))   # 能召回上次那条错题
```

若 PASM 核心可用（`tier=core/bionic`），`report` 还会把分数转成强化量
（`delta = score - 0.5`）驱动核心的学习层。

## 6. 交互模式

```bash
pasm-agents run tutor --id=my_tutor --persona-file=personas/xiaoya.json
```

直接打字对话。可用命令：

| 命令 | 作用 |
|---|---|
| `report <知识点> <0~1 分数>` | 记录一次作答，返回新掌握度 |
| `next` | 看下一个该练的知识点 |
| `snapshot` | 导出学情 JSON |
| `mood` | 看当前情绪 |
| `act` | 执行一个动作 |
| `observe <文本>` | 手动写一条记忆 |
| `feedback <praise\|poke\|scold> [动作]` | 给反馈 |
| `quit` | 退出并 save |

## 7. 档位透明

| tier | 含义 | 何时启用 |
|---|---|---|
| `bionic` | 仿生：完整 PASM 核心 + emotion 模块（需 torch） | `pip install pasm-agents[torch]` |
| `core`    | 完整：PASM 核心（memory + learning，无 torch） | `PASM_PYTHON` 指向带核心的 Python |
| `light`   | 轻量：纯内置（重要度淘汰 + 字面检索 + softmax 权重） | 任何机器 |

## 8. 已知短板（如实说明）

- **没有遗忘曲线**：掌握度只增不减，停练的知识点**不会自动衰减**。
  `study-tutor` 验证智能体用"前 5 天练、之后彻底停练"的场景测过，`decay_works = 0`。
  需要衰减的话，调用方可以定期 `report(topic, 更低的分)` 手动拉低 —— 但那是绕路，不是内置能力。
- **跨表述检索是字面匹配**：`memvec` 是字符 n-gram 哈希，不是语义模型。
  换个说法问同一个知识点，未必召回得到。

这两条改的是**产品行为**而非缺陷，所以本仓选择如实标注、不偷偷糊上去。

## 9. 与验证层的关系

本仓的 `pasm_agents/verifiers/study_tutor.py` 是**专门验证这类教学智能体的智能体**：
跑 30 天 × 4 题 × 6 个知识点，测学情结构对不对、有没有遗忘机制、错题关联能不能召回。
`snapshot()` 的形状与它定义的学情结构一致，所以**上层画像层可以直接复用同一套字段**。

## 10. 相关技能

- `pasm-npc` —— 游戏 NPC 智能体
- `pasm-companion` —— 老人陪伴智能体
- `pasm-longterm-verify` —— 验证层入口：回答"跑久了还是好的吗"
