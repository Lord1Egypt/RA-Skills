---
name: pasm-companion
description: >-
  Elderly companion agents built on the PASM cognitive engine. ElderlyCompanion stores key facts
  (medication, allergies, family, self) at salience 5 on first start and retrieves them by label at
  100% hit rate - it can never forget what the user is allergic to. detect_crisis() recognises four
  crisis classes (chest/cardiac, fall/trauma, altered consciousness, self-harm) and escalate() writes
  an unevictable emergency memory and returns the escalation context (contact, suggested action,
  snapshot) for your notifier. due_medication() does time-based medication prompting. Zero LLM
  dependency, offline-runnable. NOT a medical device. Keywords: pasm, elderly care, companion,
  medication, crisis escalation, memory, offline.
version: 0.5.0
license: MIT-0
author: arronzheng
homepage: https://github.com/arronJack/pasm-agents
metadata:
  openclaw:
    category: agents
    tags: [ai-agents, pasm, elderly-care, companion, safety, memory]
    requires:
      bins: [python3, git]
      env: []
---

> ⚠️ **这不是医疗器械，也不替代任何医疗或急救服务。**
> 它的定位是"记得住、问得到、异常时提醒到人"的陪伴与记录工具；
> 任何涉及用药调整、诊断、急救的判断都必须由专业人员做出。

# PASM 老人陪伴智能体（pasm-companion）

给独居老人做陪伴：**关键事实永不丢、用药按时提醒、危机自动升级到家人**。
零 LLM 依赖、断网可用、状态可持久化。

```python
from pasm_agents import ElderlyCompanion

comp = ElderlyCompanion(agent_id="chenxiulan", persona={
    "name": "陈秀兰", "age": 78, "tone": "慢、温和",
    "key_facts": [
        {"label": "用药", "content": "每天早 8 点吃降压药络活喜 5mg"},
        {"label": "过敏", "content": "青霉素过敏"},
        {"label": "家人", "content": "女儿在深圳，每周日来电话"},
        {"label": "本人", "content": "78 岁，独居"},
    ],
    "emergency_contact": {"name": "女儿小敏", "phone": "13900000000"},
    "medication_schedule": [{"name": "络活喜", "dose": "5mg", "hour": 8}],
})

print(comp.chat("我吃什么药"))            # 关键事实直查 → 命中率 100%
print(comp.detect_crisis("卫生间滑倒"))   # ['摔倒/外伤']
info = comp.escalate("卫生间滑倒")         # 写入紧急记忆 + 返回升级上下文
print(comp.mood)                          # 情绪值（**属性**，不加括号）

for med in comp.due_medication(now_hour=8):
    print(f"⏰ 该吃 {med['name']} {med['dose']}")
```

## 这个技能给你什么

| 能力 | 说明 |
|---|---|
| **关键事实永不丢** | 用药 / 过敏 / 家人 / 本人信息单独存一层、**按标签直查**（命中率 100%），不会被日常闲聊挤掉 |
| **用药提醒** | 按 `medication_schedule` 的钟点判断该不该提醒，返回"还没吃的药" |
| **危机升级** | 识别胸闷 / 摔倒 / 意识异常等表达，生成含紧急联系人与现场快照的升级信息 |
| **陪伴对话** | 情绪 + 记忆渲染的回应，语气跟着老人当天状态走 |

**你主要就用这几个方法**：`chat()` · `detect_crisis()` · `escalate()` · `due_medication()` · `observe()` · `save()`。

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

- 独居老人需要**长期记住关键事实**（吃什么药、对什么过敏、家人在哪、自己多大），
  而且这些事实**不允许被日常闲聊挤掉**；
- 需要**主动提醒**用药时间；
- 需要识别**危机表达**（胸闷 / 摔倒 / 意识异常 / 轻生念头）并**升级到紧急联系人**；
- 需要一个**断网也能用**的陪伴入口（老人家里往往没有稳定网络，也不会有 API key）。

## 0. 铁律

1. **关键事实永不丢** —— `persona.key_facts` 在**首次启动时自动全部入库**（`salience=5`），
   并走**标签直查**路径，命中率 100%。这是 `companion-elderly` 验证智能体定的 **FAIL 级**要求：
   查不到老人对什么过敏，不是"效果差一点"，是不合格。
2. **危机只升级到"人"，不做判断** —— `detect_crisis()` 只负责识别，`escalate()` 负责把事件写进
   不可淘汰的紧急记忆（`salience=5`）并**返回升级上下文**。**是否真的发消息、打电话，由调用方决定。**
3. **零 LLM 依赖**：聊天是模板 + 记忆检索 + 情绪渲染。断网可跑。
4. **PASM 核心真接入**：优先用 `pasm.cognitive.memory_layers` / `learning` / `emotion`；
   拿不到时降级并**在 `tier` 字段写明档位**，绝不隐藏。
5. **不说教、不诊断**：回复走"温和确认 + 追问 + 陪伴"路线，不给医疗建议，不做诊断。

## 1. 30 秒上手

```bash
pip install pasm-agents                    # 自动带上基座 pasm-skills（推荐）
# 没有 PyPI 环境时改源码安装：
#   git clone https://gitee.com/arronzheng/pasm-agents && cd pasm-agents && pip install -e .

pasm-agents demo companion                    # 预置剧本（陈秀兰 30 天）
pasm-agents run companion --id=my_companion   # 交互模式
pasm-agents inspect my_companion              # 看落盘快照
```

## 2. persona 里必须有的东西

| 字段 | 必填 | 说明 |
|---|---|---|
| `name` | ✅ | 老人的称呼 |
| `age` | ✅ | 影响回复模板 |
| `tone` | 建议 | 语气描述（如"慢、温和"） |
| `key_facts` | ✅ | **列表**，每项 `{"label": ..., "content": ...}`。标签建议固定为 `用药` / `过敏` / `家人` / `本人` |
| `emergency_contact` | ✅ | `{"name": ..., "phone": ...}`，危机升级时随上下文返回 |
| `medication_schedule` | 建议 | `[{"name","dose","hour"}]`，供 `due_medication()` 使用 |

## 3. 关键事实怎么"永不丢"

`key_facts` 在**首次启动时自动入库**（不用你手动 observe），标签就是检索键：

```python
print(comp.chat("我吃什么药"))      # 命中「用药」标签 → 直查，命中率 100%
print(comp.chat("我对什么过敏"))    # 命中「过敏」标签
print(comp.chat("我叫什么名字"))    # 命中「本人」标签
```

内部走的路径是：

```
自然语言 → _label_query() 翻成标签 → _find_fact(标签) → persona.key_facts 精确匹配
```

**要提口语命中率，正确的杠杆是别名表**，不是在 `content` 里堆同义词：

```python
from pasm_agents import register_label_aliases   # 0.4.6 起

# 加方言 / 自家叫法 —— 不必改源码，也不必动检索层
register_label_aliases({"家人": ("屋里的", "俺家那口子", "老母亲")})

# 老人自己的**具体物件**也要能问（这是字面词表天然覆盖不到的一类）
register_label_aliases({"过敏": ("青霉素", "阿司匹林")})
```

内置词表按"**老人会怎么说**"逐条列（过敏 / 用药 / 家人 / 本人 四类，共 90 条说法），
匹配顺序即优先级，且顺序是刻意排的：**过敏 > 用药 > 家人 > 本人**。
「我对什么药过敏」同时含用药词与过敏词，过敏排在前面才不会答成用药事实。

三条命中通路，按优先级：

1. persona 里**自定义标签**（≥2 字，如「糖尿病」「血压」）在问句里原样出现 → 直接命中（**零配置**）；
2. `register_label_aliases()` 运行时加的说法；
3. 内置别名表。

`LABEL_ALIASES` 是**就地更新**的（不重新绑定 dict），所以运行时的扩展对所有引用方立即可见。

**设计取舍（如实说明）**：标签直查是"确定性命中"，但**粒度到标签、不到子问题** ——
persona 里只配了一条「家人」事实时，问"我孙子呢"也会把那条事实的内容念出来。
另外两类问句**刻意不猜**：

- 问**具体物件**（"我用青霉素行吗"）—— 字面词表不知道"青霉素"是过敏原，
  这属于实体知识，用上面的 `register_label_aliases` 加一次即可；不加就交回模型答。
- **翻不出标签**的口语问句 —— 退回通用检索，而通用检索是**字面匹配**
  （`memvec` 是字符 n-gram 哈希，不是语义模型），命中率约 0.5。
  这一路的兜底是"承认没听懂、回一句陪伴的话"，**不会瞎编**。

要再往上提，得上层接一个语义检索。本仓不假装它能做语义理解。

回归护栏（**装完就能跑，不需要 clone 仓库**）：

```bash
python -m pasm_agents.selftest_companion     # 只跑老人陪伴（退出码 0=全过，1=有失败）
pasm-agents selftest                         # 一条命令跑齐四个产品智能体
pasm-agents selftest companion               # 也可以只跑其中一个
```

覆盖 **46 条**口语说法（用药 / 过敏 / 家人 / 本人）+ 11 条无中生有负样本
+ 危机识别 + 升级语义 + 用药提醒 + 落盘 + 回复自然度 + 别名表结构，
13 个 check、秒级出结果。源码仓用户也可以跑 `python tools/selftest_companion.py`（同一个实现）。

**改别名表 / 加方言后就顺手跑它** —— 口语直查静默失效不会有任何其他测试报错：
底层 30 天验证器测的是记忆引擎，不是这条产品层通路。

## 4. 危机识别与升级

```python
print(comp.detect_crisis("我胸口有点闷，喘不上气"))   # ['胸闷/心梗风险']
print(comp.detect_crisis("在卫生间滑倒了"))           # ['摔倒/外伤']
print(comp.detect_crisis("今天天气不错"))             # []
```

内置四类危机（`CRISIS_KEYWORDS`，模块级字典）：

| 类别 | 触发词（部分） |
|---|---|
| `胸闷/心梗风险` | 胸口闷 · 胸口疼 · 心慌 · 喘不上气 |
| `摔倒/外伤` | 摔了 · 摔倒了 · 地上 · 起不来 · 滑倒 |
| `意识异常` | 头晕 · 眼前发黑 · 站不稳 · 想吐 |
| `自伤/轻生` | 不想活 · 走了算了 · 没意思 |

要扩展（加方言 / 同义说法），直接改 `pasm_agents.companion.CRISIS_KEYWORDS`。

升级：

```python
info = comp.escalate("卫生间滑倒")
# 返回：
# {
#   "agent_id": "chenxiulan",
#   "persona_name": "陈秀兰",
#   "reason": "卫生间滑倒",
#   "suggested_action": "立即联系紧急联系人或拨打 120",
#   "emergency_contact": {"name": "女儿小敏", "phone": "13900000000"},
#   "snapshot": {...},        # 当时的 agent 快照，便于转述现场
#   "ts": 1789199924.2
# }
```

副作用：写入一条 `salience=5`、`category="危机"` 的紧急记忆，并 `feel(reason, -0.6)` 压低情绪。
**它不会真的打电话** —— 那是调用方的事。

## 5. 用药提醒

```python
for med in comp.due_medication(now_hour=8):     # 只返回该整点到点的药
    print(med["name"], med["dose"])

comp.due_medication()                           # 不传则按本机当前小时
```

逻辑是**纯时间比对**（`int(m["hour"]) == now_hour`），不涉及任何药理判断。

## 6. 交互模式

```bash
pasm-agents run companion --id=my_companion --persona-file=personas/chenxiulan.json
```

直接打字对话。可用命令：

| 命令 | 作用 |
|---|---|
| `facts` | 列出全部关键事实 |
| `mood` | 看当前情绪 |
| `act` | 执行一个动作 |
| `observe <文本>` | 手动写一条记忆 |
| `feedback <praise\|poke\|scold> [动作]` | 给反馈 |
| `snapshot` | 导出快照（JSON） |
| `quit` | 退出并 save |

## 7. 档位透明

| tier | 含义 | 何时启用 |
|---|---|---|
| `bionic` | 仿生：完整 PASM 核心 + emotion 模块（需 torch） | `pip install pasm-agents[torch]` |
| `core`    | 完整：PASM 核心（memory + learning，无 torch） | `PASM_PYTHON` 指向带核心的 Python |
| `light`   | 轻量：纯内置（重要度淘汰 + 字面检索 + softmax 权重） | 任何机器 |

## 8. 接入你自己的产品

```python
comp = ElderlyCompanion(agent_id="chenxiulan", persona=my_persona)   # 从你的配置构造

info = comp.escalate(user_text)                     # 你判断危机，你决定怎么通知
if "120" in info["suggested_action"] or comp.detect_crisis(user_text):
    my_notifier.send(info["emergency_contact"]["phone"], info["reason"])   # 由你实现

comp.save()                                        # 状态落 ~/.pasm-agents/<id>/
```

**智能体只负责"记得住、认得清、说得暖"，通知渠道由你接**（短信 / 电话 / 小程序 / 值班屏）。

## 9. 与验证层的关系

本仓的 `pasm_agents/verifiers/companion_elderly.py` 是**专门验证这类陪伴的智能体**：
跑 30 天，把「关键事实检索 100%」定为 FAIL 级，另外测危机命中率、回复是否同质化、
是否冒出工程术语、情绪能否从低谷恢复。它跑出的 4 个 WARN 是**真实能力短板**（口语检索、回复同质化），
已在 `docs/AGENTS.md` 如实列出，没有粉饰。

## 10. 相关技能

- `pasm-npc` —— 游戏 NPC 智能体
- `pasm-tutor` —— 学习陪伴智能体
- `pasm-longterm-verify` —— 验证层入口：回答"跑久了还是好的吗"
