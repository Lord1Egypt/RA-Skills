---
name: pasm-cs-agent
description: >-
  Customer-service agents built on the PASM cognitive engine. CustomerServiceAgent answers only from
  knowledge facts (entries carrying a source) and applies a relevance gate that requires the match to
  land on the entry's title or tags - so it refuses to answer instead of answering the wrong thing
  (measured: true hits score 6.0-24.5 while a bogus hit via one incidental word scored 2.29).
  Complaint phrases in four classes are detected and escalated into salience-5 memory that small talk
  can never evict, returning escalation context for your notifier. Knowledge is ingested incrementally
  with content-fingerprint de-duplication, and each agent gets its own KB directory so multiple
  tenants on one host cannot leak into each other. Optional vendor-neutral LLM with automatic fallback
  to KB answering. Keywords: pasm, customer service, knowledge base, FAQ, escalation, offline.
version: 0.5.0
license: MIT-0
author: arronzheng
homepage: https://github.com/arronJack/pasm-agents
metadata:
  openclaw:
    category: agents
    tags: [ai-agents, pasm, customer-service, knowledge-base, support, offline]
    requires:
      bins: [python3, git]
      env: []
---

# PASM 智能客服智能体（pasm-cs-agent）

给站点 / 平台做一个**就资料作答、答不上来如实说、客诉自动转人工**的客服智能体。
资料库可增量喂养，可选接大模型，状态可持久化。

```python
from pasm_agents import CustomerServiceAgent

cs = CustomerServiceAgent(agent_id="shop_cs", persona={
    "name": "小智", "role": "售后客服",
    "tone": "温暖、专业、耐心",
    "hotline": "400-000-0000",
})

print(cs.answer("怎么退货？"))              # 就资料作答 + 标注资料来源
print(cs.answer("你们能送到火星吗？"))       # 查不到 → 如实说不知道（不编造）
print(cs.answer("我要投诉你们，再不处理就曝光！"))   # 自动标记转人工

cs.ingest_faq([{                            # 增量喂自己的业务知识
    "title": "会员日优惠",
    "content": "每月 8 日会员日，黄金会员全场额外 9 折。",
    "source": "faq", "tags": ["会员", "优惠"],
}])
print(cs.kb_stats())        # 资料库规模
print(cs.snapshot())        # 可机读状态（接监控 / 运营看板）
```

## 这个技能给你什么

| 能力 | 说明 |
|---|---|
| **就资料作答** | 检索资料库作答并**标注资料来源**；查不到就如实说不知道，**绝不编造** |
| **相关性闸门** | 命中必须落在条目的**标题或标签**上，挡住"靠正文里一个偶然重合的词"造成的**答非所问** |
| **客诉转人工** | 四类必须人工的表达（投诉/曝光、法律/监管、安全/伤害、要求赔偿）自动识别，写入不可淘汰记忆并返回升级上下文 |
| **资料库自生长** | `ingest_faq()` 增量喂养，反复喂同一条不会重复膨胀（内容指纹去重） |
| **资料库按智能体隔离** | 每个智能体一个库（`<persist_dir>/kb`），同机多租户**不会串库** |
| **可机读快照** | `snapshot()` 输出纯 dict（资料库规模 / 情绪 / 交互数 / 客诉次数 / 档位） |
| **可选接大模型** | 传 `llm={...}` 走 LLM 作答；LLM 不可用时**回落到资料库作答**，永远有回应 |

**你主要就用这几个方法**：`answer(text)` · `ingest_faq(items)` · `needs_escalation(text)` · `escalate(text)` · `kb_stats()` · `snapshot()` · `save()`。

## 它跑在什么之上：基座 `pasm-skills` + 应用框架 `pasm-framework`

| | 是什么 | 装它 |
|---|---|---|
| **pasm-skills**（基座） | 只提供能力，**不含任何智能体** | `pip install pasm-skills` |
| **pasm-framework**（应用框架） | 应用级表面：插件子系统 / 资料库 / HTTP 网关 / 流式输出 | `pip install pasm-framework` |
| **pasm-agents**（本技能来源） | 游戏 NPC / 老人陪伴 / 学习陪伴 / 智能客服 + 7 个验证智能体 | `pip install pasm-agents` |

> 装 `pasm-agents` 会**自动带上基座与框架**，一条命令搞定。

**本产品与另外三个有一处实质差别，知道它能省你很多时间**：
另外三个建在基座的 `BaseAgent` 上；客服建在框架的 `BaseApplication` 上。
原因很直接 —— "客服"的核心能力是**资料库**，而资料库是框架的 `knowledge_base` 插件，
**不是基座 SDK 里有的东西**。所以客服在 `tier=light`（纯标准库）时，
资料库依然完整可用，不像另外几个产品那样在轻量档下丢掉部分能力。

> ⚠️ 由此带来一个你必须知道的**构造参数差异**：客服支持 `kb_dir=` / `persist_dir=` 传路径。
> 跑多个客服（多家店 / 多租户）时**务必各给一个 `persist_dir`**，否则会共用默认落点。

## 什么时候用

- 需要一个**基于自有资料**作答、而不是"张口就编"的客服；
- 需要**答不上来时如实说**、并把问题上交（而不是硬凑一个答案）；
- 需要**自动识别客诉**并转人工（投诉、法律、安全事故、索赔）；
- 需要把客服**同时**接成：程序内调用 / HTTP 接口 / 站点挂件 / 大模型平台的工具（MCP）。

## 0. 铁律

1. **不许编造**。`_render_reply` 只认 `knowledge_facts(facts)` —— 也就是**带 `source` 的知识**，
   引擎的对话记忆（不带 `source`）一律不作为答案来源。
   这条过滤不能省：否则"上一轮用户自己说过的话"会被当成资料答回去。
2. **答非所问比答不上来严重**。所以有第二道闸门 `touches_surface()`：
   命中必须落在条目的**标题或标签**上，**或**分数达到 `score_floor`（默认 `4.0`）。
   - 实测依据（在起步资料库上，不是拍脑袋）：真命中分数 **6.00 ~ 24.50**；
     假命中例如问「请问 CEO 的私人邮箱是多少」，靠正文里一个「邮箱」命中了**发票开具**，分数 **2.29**。
   - 为什么主判据不用绝对分数：分数带**时间衰减**（`0.6 + 0.4 × recency`），
     资料库放一个月后真命中会被压到原来 0.6 倍，任何固定阈值都会开始"失忆"。
     而"命中落在标题/标签上"与分数、与时间**都无关**。
3. **客诉词表只收明确指向该场景的说法，判不出来就放行**。
   - 元组用**短语**而非单字：「退款」是正常问询，「**要求**退款」才是客诉；
   - 安全类只收**结果性**表达：「过敏了 / 受伤了」，**不收**光杆「过敏 / 受伤」——
     因为「这个成分会让我过敏吗」是提问，升级它等于乱升级。
   - 回归护栏：`python -m pasm_agents.selftest_customer_service`（75 项，秒级，退出码 0/1）。
4. **客诉记忆不可被挤掉**：`escalate()` 按 `salience=5` 写入，日常闲聊挤不掉它，事后复盘一定查得到。
5. **资料库按智能体隔离**：默认落在 `<persist_dir>/kb`，**不跟随**插件那个全机共享的
   `~/.pasm_framework/kb`。同机跑多个客服时必须各给 `persist_dir` ——
   不隔离的后果属于**跨租户数据泄漏**（A 店的 FAQ 会被检索进 B 店的答复里）。
6. **网关默认关**。`serve()` 前必须构造时传 `enable_gateway=True`，否则框架直接抛
   `FrameworkError` —— 这是**故意的**，避免任何一次 `serve()` 意外占住 8080 端口。

## 1. 30 秒上手

```bash
pip install pasm-agents                    # 自动带上基座与框架（推荐）
# 没有 PyPI 环境时改源码安装：
#   git clone https://gitee.com/arronzheng/pasm-agents && cd pasm-agents && pip install -e .

pasm-agents demo customer-service          # 预置剧本：就资料作答 / 查不到 / 客诉 / 增量喂料
pasm-agents run customer-service --id=my_cs    # 交互模式
pasm-agents inspect my_cs                  # 看落盘快照
pasm-agents selftest customer-service      # 跑本产品的自测护栏
```

或直接从源码跑（`pip install` 之后可删掉脚本里的 `sys.path` 引导）：

```bash
python agents/product/customer_service/quickstart.py
```

## 2. persona 里可配的东西

| 字段 | 必填 | 说明 |
|---|---|---|
| `name` | 建议 | 客服称呼（默认「小智」） |
| `role` | 建议 | 角色（默认「智能客服」） |
| `tone` | 建议 | 语气（默认「温暖、专业、耐心」） |
| `hotline` | **强烈建议** | 客服热线。**转人工提示与兜底回复都会引用它**；不填则回复只说"联系我们的客服"，用户拿不到号码 |
| `temper` / `energy` / `play` | 否 | 性格参数，影响情绪与动作倾向 |

```python
cs = CustomerServiceAgent("shop_cs", persona={
    "name": "小智", "role": "售后客服", "hotline": "400-820-8820",
})
```

**构造参数**（都是关键字参数）：

| 参数 | 默认 | 说明 |
|---|---|---|
| `kb_dir` | `<persist_dir>/kb` | 资料库目录。多租户隔离的抓手 |
| `persist_dir` | `~/.pasm-agents/<agent_id>` | 状态与资料库根目录 |
| `seed_faq` | `True` | 是否首次启动灌入起步资料（5 条通用 FAQ）。换成自己的业务知识时传 `False` |
| `llm` | `None` | 形如 `{"provider": ..., "model": ...}`；传了才启用 LLM 作答 |
| `enable_gateway` | `False` | 是否启用 HTTP 网关（`serve()` 的前置条件） |
| `serve_port` | `8080` | 网关端口 |
| `score_floor` | `4.0` | 相关性闸门的次级门槛（见铁律 2） |

> `seed_faq=True` 的理由与老人陪伴"首次启动写入关键事实"同一套思路：
> **用户的第一次体验必须能答上来**，而不是"资料库是空的，请先喂资料"。
> 是否灌过记在 `state.notes["cs_faq_seeded"]` 里（一次性标记，语义明确），
> 灌失败也会留痕（例如资料库插件被关掉时记 `"skipped(no knowledge_base)"`），
> 免得"我明明喂了资料为什么答不上来"变成最难查的一类问题。

## 3. 作答与客诉

```python
cs.answer("怎么退货？")
# -> 关于您的问题，我们查到相关说明：签收后 7 天内支持无理由退货……（资料来源：faq）

cs.answer("你们能送到火星吗？")
# -> 抱歉，我暂时没有查到关于这个问题的资料，已记录您的问题。您可以拨打我们的客服热线 400-…，或稍后再试。

cs.answer("我要投诉你们，再不处理就曝光！")
# -> <资料库答复>
#    【已标记转人工｜投诉/曝光】您的诉求我已记录，会由专人跟进；如需立刻处理请拨打 客服热线 400-…
```

`answer()` 是 `handle()` 的业务化封装，比裸 `handle()` 多一件事：
命中客诉判据时**在回复末尾追加转人工提示**并把这次客诉记进记忆 ——
"客服"与"普通聊天机器人"的实质区别就在这儿。

只想**预筛**、不想构造智能体也行（同一套判据，不会两边跑偏）：

```python
from pasm_agents import detect_escalation

detect_escalation("我要起诉你们")     # -> '法律/监管'
detect_escalation("要求赔偿三倍")      # -> '要求赔偿'
detect_escalation("这个功能真难用啊")   # -> None（普通抱怨，不升级）
```

`escalate()` 返回给**你的通知渠道**用的升级上下文：

```python
esc = cs.escalate("我要投诉你们", session_id="s-42", user_id="u-1001")
# {'agent_id':…, 'reason':'投诉/曝光', 'text':…, 'session_id':'s-42', 'user_id':'u-1001',
#  'hotline':'400-…', 'escalation_count':1, 'created_at':…}
# 把它丢给工单系统 / 企业微信 / 飞书机器人即可。
```

## 4. 喂养自己的业务知识

```python
cs.ingest_faq([
    {"title": "会员日优惠", "content": "每月 8 日会员日，黄金会员全场额外 9 折。",
     "source": "faq", "tags": ["会员", "优惠"]},
    {"title": "对公转账", "content": "企业客户可在结算页选择「对公转账」并填写开票信息。",
     "source": "faq", "tags": ["支付", "对公"]},
])

print(cs.kb_stats())   # {'total': 7, ...} 之类
```

| 字段 | 必填 | 说明 |
|---|---|---|
| `title` | ✅ | 标题。**它同时是检索面** —— 闸门就靠标题和标签判断相关性，取个能被搜到的名字 |
| `content` | ✅ | 正文 |
| `source` | 建议 | 来源标记。**带 `source` 才被当作"知识"**（缺了它不算资料） |
| `tags` | **强烈建议** | 标签，与标题一起构成检索面。用户的口语词尽量覆盖进来 |

> **反复喂同一条不会重复膨胀**：连接器按内容指纹去重，
> 同一份资料每天同步一次也只留一份。
> 如果你在做一个会**定时从业务库同步**的客服，配套的 `pasm-customer-service`
> 里有现成的 DB→KB 同步连接器（见第 9 节）。

## 5. 状态快照

```python
print(cs.snapshot())
# {
#   "agent_id": "shop_cs",
#   "persona": {...},
#   "tier": "light",
#   "mood": 0.5,
#   "interactions": 12,
#   "kb": {"total": 5, ...},
#   "escalations": 1,
#   "faq_seeded": 5
# }
```

接监控 / 后台报表 / 运营看板都直接用这个 —— 不用解析自然语言，
也不用伸手进内部字典。`kb` 在未启用资料库插件时是 `None`（**不假装有**）。

## 6. 接大模型（可选）

```python
cs = CustomerServiceAgent("shop_cs", llm={
    "provider": "openai-compatible",
    "model": "your-model",
    "base_url": "https://...",
    "api_key": "...",
})
```

开了 LLM 后由模型组织语言，**但资料仍来自你的资料库**（检索结果作为上下文注入）。
LLM 不可用时会**自动回落到资料库作答** —— 保证永远有回应，而不是给用户一个报错。

本产品**不绑定任何模型厂商**：`llm` 是普通配置字典，接哪家由你定。

## 7. 档位透明

| tier | 含义 | 何时启用 |
|---|---|---|
| `bionic` | 仿生：完整 PASM 核心 + emotion 模块（需 torch） | `pip install pasm-agents[torch]` |
| `core`    | 完整：PASM 核心（memory + learning，无 torch） | `PASM_PYTHON` 指向带核心的 Python |
| `light`   | 轻量：纯标准库 | 任何机器 |

**客服在 `light` 档下资料库功能完整**（资料库属于框架层，见前面"它跑在什么之上"）。
档位只影响记忆与情绪的深度，不影响"能不能就资料作答"。

## 8. 已知短板（如实说明）

- **检索是词面匹配，不是语义理解**：资料库打分基于「重叠词 × 字段权重 + 精确率」，
  不是向量语义模型。用户换个完全不同的说法问同一件事，可能召回不到 ——
  补救办法是把**口语说法写进 `tags`**（标签就是检索面）。
- **相关性闸门是保守取向**：它宁可说"查不到"也不答非所问。
  代价是**边界情况会偏保守**（该答的可能答不上）。若你的场景更怕"答不上来"，
  把 `score_floor` 调低即可（调低＝放宽）。
- **不是工单系统**：它识别客诉、记录、给出升级上下文，但**派单 / 排班 / 结单要接你自己的系统**。
- **没有内置的会话鉴权**：`user_id` 只是透传字段。对外暴露网关时，鉴权由你的接入层负责。

这三条改的是**产品定位**而非缺陷，所以如实标注，不偷偷糊上去。

## 9. 想要"完整客服系统"而不只是一个智能体

本技能给的是**智能体**。如果你要的是开箱可跑的整套 ——
**DB→KB 定时同步连接器 + 真 MCP 服务 + 浏览器聊天壳 + 桌面端一键加载** ——
那是独立发布的 **`pasm-customer-service`**：

```bash
pip install pasm-customer-service
pasm-cs run --source sqlite     # 业务库 → 资料库 增量同步（有 updated_at 就只抓变更行）
pasm-cs web                     # 浏览器聊天壳（普通人直接打开就能聊）
pasm-cs mcp                     # 真 stdio MCP 服务，供大模型平台调用
pasm-cs studio                  # 生成桌面端场景配置
```

| 你要什么 | 用哪个 |
|---|---|
| 代码里嵌一个客服 | 本技能的 `CustomerServiceAgent` |
| 从业务库**自动同步**资料进来 | `pasm-customer-service` 的 `pasm-cs run` |
| 给同事/客户一个**网页**直接聊 | `pasm-customer-service` 的 `pasm-cs web` |
| 让 **Claude / WorkBuddy** 等平台调用你的客服 | `pasm-customer-service` 的 `pasm-cs mcp` |

> 两者共用同一套"就资料作答 + 客诉转人工"内核，不是两份实现。

## 10. 相关技能

- `pasm-npc` —— 游戏 NPC 智能体
- `pasm-companion` —— 老人陪伴智能体（同样有"危机识别 + 不可淘汰记忆"）
- `pasm-tutor` —— 学习陪伴智能体
- `pasm-longterm-verify` —— 验证层入口：回答"跑久了还是好的吗"
