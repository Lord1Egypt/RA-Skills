# 商品认知录入助手 · 提示词包(product-cognition-intake)

> 平台无关的"商品认知录入"skill 包。目的:让运营/商家在**任意 AI 平台**(豆包 / 扣子 Coze / Dify / 自研 Bot)上,把商品核心认知整理成**严格冒号软标签**文本,系统侧 **0 模型**规则解析入库,供 AI 导购意图识别与召回使用。

## 这个包是什么

一份"契约 + 两种引入壳 + 示例"的**混合包**。核心是 `规范.md`(唯一事实源),外面套两种引入形态:`SKILL.md`(给聊天 agent 按需调用)、`system-prompt.md`(给专用 Bot 当人设)。

| 文件 | 作用 |
|---|---|
| `规范.md` | **唯一契约源**:严格软标签全集、行首规则、受控词、合规红线、判定阈值。改标签只改这里 |
| `SKILL.md` | **给聊天智能体**:Agent Skill 壳(YAML 头 + 引导流程),按需触发、不替换 agent 人设,渐进披露读 `规范.md`/`examples.md` |
| `system-prompt.md` | **给专用 Bot**:可直接复制的录入助手人设(整段粘进 System Prompt) |
| `examples.md` | 认知卡 few-shot(水牛奶 / 土鸡蛋 / 5号电池)+ 反例 |
| `changelog.md` | 版本记录;标签改动须同步两处解析器 |

## 两种引入形态(按"引入方"选)

### A. 专用录入 Bot(整个 Bot 就是录入助手)→ 用 `system-prompt.md`
**通用 3 步**:
1. 新建一个 Bot/智能体/App。
2. 把 `system-prompt.md` 整段复制进「人设 / System Prompt / 提示词」。
3. (可选)把 `examples.md` 作为知识/示例补充。

- **豆包 / 扣子(Coze)**:新建 Bot →「人设与回复逻辑」粘 `system-prompt.md`。
- **Dify**:新建「聊天助手」App →「提示词」粘 `system-prompt.md`;`examples.md` 可入知识库。
- **自研 / OpenAI GPT / 其他**:把 `system-prompt.md` 作为 system message。

### B. 多能力聊天智能体(录入只是它众多能力之一)→ 用 `SKILL.md`
- **不要**把 `system-prompt.md` 塞进人设——那会把多能力 agent 变成只会录入的 Bot。
- 支持 Agent Skills 的 harness(Claude Code / Agent SDK 等):把本目录作为一个 skill 挂载,agent 按 `SKILL.md` 的 `description` **自动触发**,用到才读 `规范.md`。
- 不支持 SKILL.md 的平台:把 `SKILL.md` 正文作为一段"当用户要录入商品时,按此引导"的**分支指令**并入 agent 提示词(而非整体人设),`规范.md` 作为参考资料。

运营/用户对话录入 → 产出规范 intro 文本 → **原样复制**贴进商品平台的「商品简介 / ai_product_intro」字段。

## ⚠️ 同源约束(重要)

`规范.md` 的标签名 / 行首规则 / 受控词,与**两处规则解析器严格对齐**:
- Python:`app/retrieval/intro_parser.py`(LLM 兜底路径)
- Java(mall):`IntroSoftSpecParser`(商品变化接收链路直落,见 `p_java_gns_node/docs/superpowers/specs/2026-08-19-intro-softspec-rule-parse-design.md`)

**改任何标签名/别名/阈值,必须同步改这两处解析器 + 本包 `规范.md` + `system-prompt.md`**,否则运营写的东西系统识别不了。

## 上位设计
- 软规范:`docs/superpowers/specs/2026-08-17-product-intake-softspec-design.md`
- 商品认知知识库总纲:`docs/知识库/00-总纲-商品认知知识库.md`
- 产品方案认知卡:`AI导购系统产品方案V1.0` §4.3 / §9.1
