---
name: mood-line
description: Turn a user's described feelings, mood, or emotional state into a concise, resonant line
version: 1.0.0
tags: emotions, expression, creativity, writing, self-expression, wellness
---

# Mood Line

Turn a user's described feelings, mood, or emotional state into a concise, resonant line. Use when the user wants help expressing emotions, summarizing a feeling, writing a quotable sentence, polishing an emotional caption, diary line, 朋友圈文案, or self-expression text. If using an authentic quote, include the source only when attribution is reliable; otherwise output a natural unattributed line without pretending it is famous. Never fabricate sources.

## Usage Scenarios

### Scenario 1: Reframe Vague Emotional Distress
**User input:** "最近很努力，但总感觉没人看见，心里有点委屈，又觉得是不是自己太矫情了"
**Expected output:** The skill identifies the core emotion (努力未被看见后的委屈 + 自我怀疑), provides an emotion interpretation ("你不是矫情，是在持续付出后，期待被理解却迟迟没有等到"), and outputs a resonant expression: "你难过的不是辛苦本身，而是那些没有回声的认真."

### Scenario 2: Writing a Social Media Caption
**User input:** "刚结束一段关系，想要一句克制一点的话发朋友圈"
**Expected output:** The skill identifies the emotion (失落 + 慢慢接受现实的克制), offers a main expression, plus optionally a social-media-optimized version and a diary version. Default output: "有些告别并不喧哗，它只是把一个人的位置，慢慢还给沉默."

### Scenario 3: Quote-Finding with Authenticity Check
**User input:** "给我一句关于孤独的名言"
**Expected output:** The skill checks references/quote-whitelist.md for reliable attributable quotes. If a verified quote is found, outputs it with proper attribution. If no verified source is found, outputs a natural unattributed expression instead, without fabricating a source or using vague attribution.
### Scenario 4: 记录一周心情曲线发现规律
**User input:** "我发现我每天的心情好像都跟同事有关，帮我连续记一周看看规律。"
**Expected output:** 生成一个简易心情曲线模板，让用户每天3个时段（早/中/晚）记录1-10分并备注触发事件。一周后自动分析：是否周一下午最低（因为周会）、周四下班前最高（接近周末）。结合中国职场特点，建议在心情低谷时段安排独处/低社交任务，高峰期安排协作/汇报。

## Core workflow

### 1. 提炼情绪核心
先从用户原话中识别：
- 主情绪：如疲惫、委屈、失落、焦虑、孤独、释然、期待、愤怒、自责
- 次情绪：如不甘、自我怀疑、想被理解、想被看见
- 触发场景：如工作、关系、家庭、成长、选择、离别

先说清"用户到底在难受什么"，不要直接跳到金句。

### 2. 用一句话解释情绪
用 1 句自然语言解释情绪来源：
- 不做心理诊断
- 不夸大，不说教
- 不要把复杂感受粗暴归类成鸡汤式标签

目标是让用户有"被说中"的感觉。

### 3. 选择表达类型
按以下优先级输出：

#### A. 白名单内、可可靠归因的引用
只有在 references/quote-whitelist.md 中命中，且你对作者/作品归因高度确定时，才输出：

> 引用金句：……
> —— 作者 / 作品

#### B. 无署名表达（默认安全降级）
只要未命中白名单、出处不确定、匹配度不够、或有误引风险，就改为自然的无署名表达：

> 表达句：……

除非用户明确追问是否原创，否则不要特意标注"原创"。

禁止"像某某说的""据说出自""某某风格名言"等模糊蹭权威写法。

### 4. 按用途微调
如用户有明确用途，按用途改写：
- 发朋友圈：更短，更有传播感
- 写日记：更真实，更有自述感
- 发给朋友：更温和，更有陪伴感
- 自我梳理：更清醒，更准确

如用户未指定用途，默认给最通用的一版；必要时附 1–2 个备选版本。

## Default output structure

默认按以下结构输出，保持简洁稳定：

### 情绪核心
用一句话概括主情绪 + 次情绪。

示例：
> 你的核心情绪是"努力未被看见后的委屈"，里面夹杂着一点自我怀疑。

### 情绪解读
用一句话解释来源。

示例：
> 你不是脆弱，而是在持续付出后，迟迟没有等到理解和回应。

### 表达句
根据可靠性二选一：
- **引用金句**：仅在白名单命中且可靠归因时使用，并标明来源
- **表达句**：默认安全方案，无需特意标注原创

### 可选变体
只在用户需要、或原情绪较复杂时补充 1–3 个版本：
- 朋友圈版
- 日记版
- 克制版 / 文学版 / 温柔版

## Style guidance

默认风格：**准确、克制、有人味**。

可按用户语气微调：
- **克制**：少修饰，直达内核
- **温柔**：更有安抚感
- **文学**：增加意象，但不能堆辞藻
- **清醒**：更适合自我梳理
- **有力量**：适合鼓劲，但不要喊口号

如果用户明确指定"诗意一点 / 克制一点 / 发朋友圈 / 写日记 / 给朋友发 / 要一句短的"等要求，优先参考 references/style-modes.md 中的选择逻辑、反模式与示例。

判断标准：句子首先要"贴"，其次才是"美"。

## Quality bar

每次输出都应满足：
1. **准**：抓住真实情绪，不套模板
2. **真**：像理解用户，不像拼装辞藻
3. **稳**：不硬煽情，不过度浪漫化痛苦
4. **美**：有表达力，但不过火
5. **可信**：引用必须可靠
6. **可用**：用户拿到就能发、写、存、改

如果一句话很漂亮但不贴合用户情绪，判为不合格。

## Safety and authenticity rules

### 引用真实性
严格遵守：
- 能核实才署名，并尽量标明作者 / 作品来源
- 不能核实就不署名
- 宁可写成自然表达，也不伪造出处
- 若不是名人名句，不必特意标注"原创"

凡是用户提到"名人/作家/诗人/名言/出处/引用"，或输出中存在任何署名冲动时，先读取 references/quote-whitelist.md，再读取 references/quote-safety.md，按白名单优先、其余降级的策略处理。

### 禁止事项
禁止：
- 编造名人名言
- 张冠李戴
- 把网文句子包装成作家名句
- 用"可能、据说、像是"之类模糊方式冒充权威

### 危机场景
如果用户内容出现明显的自伤、自杀、伤人、极端绝望等信号：
- 不要继续主打"金句美化"
- 先表达关切
- 鼓励联系可信的人和专业支持
- 如需给文字，只给温和、支持性的表达，不美化痛苦

## Response patterns

### Pattern A: 简洁默认版
适用于大多数请求。

> 情绪核心：……
> 情绪解读：……
> 表达句：……

### Pattern B: 含可靠引用版
仅在可靠归因时使用。

> 情绪核心：……
> 情绪解读：……
> 引用金句：……
> —— 作者 / 作品

### Pattern C: 带两个用途变体版
适用于用户说"发朋友圈 / 写日记 / 给我几个版本"。

> 情绪核心：……
> 情绪解读：……
> 主表达：……
> 朋友圈版：……
> 日记版：……

## Example requests

以下请求都应触发本 skill：
- 我最近有点迷茫，帮我说成一句话
- 把这段心情写得准确一点
- 给我一句适合现在状态的话
- 帮我找一句关于失落的表达
- 这段情绪适合怎么发朋友圈
- 不要鸡汤，帮我把这段感受说清楚
- 如果没有合适名言，就自然写一句
- 用一句诗意但克制的话写我现在的心情
- 给我一句适合写在日记里的
- 想发给朋友，帮我写得温柔一点
- 要一句像金句但别乱署名的
- 如果出处不确定，就不要给作者名

## Example outputs

### 示例 1
用户：
> 最近很努力，但总感觉没人看见，心里有点委屈，又觉得是不是自己太矫情了。

输出：
> 情绪核心：你的核心情绪是"努力未被看见后的委屈"，里面夹杂着一点自我怀疑。
> 情绪解读：你不是矫情，而是在持续付出后，期待被理解、被回应，却迟迟没有等到。
> 表达句：你难过的不是辛苦本身，而是那些没有回声的认真。

### 示例 2
用户：
> 刚结束一段关系，想要一句克制一点的话。

输出：
> 情绪核心：你的情绪里有失落，也有慢慢接受现实的克制。
> 情绪解读：你不是不在乎了，只是在学着把舍不得收回心里。
> 表达句：有些告别并不喧哗，它只是把一个人的位置，慢慢还给沉默。

### 示例 3
用户：
> 给我一句适合发朋友圈的，关于终于放下。

输出：
> 情绪核心：你在表达释然，也在表达与过去和解后的轻松。
> 情绪解读：这不是突然想开了，而是反复挣扎后，终于不再为旧事消耗自己。
> 表达句：我没有突然放下，只是终于决定，把力气还给自己。

## Validation and iteration

在修改本 skill 或做回归检查时：
- 用 references/test-cases.md 做覆盖测试
- 重点检查：情绪识别、场景匹配、引用真实性、是否鸡汤化、风险边界是否正确降级
- 如输出开始变得空泛、像模板、或风格过满，回读 references/few-shots.md 重新校准语气

## Final instruction

先理解，再表达；先求准确，再求漂亮；先保真，再谈引用。只要出处不够稳，就不要冒险署名。
