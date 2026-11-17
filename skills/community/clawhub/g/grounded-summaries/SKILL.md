---
name: grounded-summaries
description: "Anti-hallucination guardrails for AI summary tasks — prevents agents from fabricating 'blank-day' content when source logs are empty. Built from a real production incident postmortem. 总结类任务的防幻觉护栏，防止 agent 在日志为空时编造内容，来自真实线上事故复盘。Keywords: anti-hallucination, grounded summary, hallucination guardrail, 防幻觉, 总结护栏, blank-day, fabrication detection"
version: "1.0.0"
author: "莫问QWQ (MoWenQWQ)"
created: "2026-08-25"
updated: "2026-08-25"
---

# Grounded Summaries — 总结类任务的防幻觉护栏
# Grounded Summaries — Anti-Hallucination Guardrails for Summary Tasks

> 本 skill 来自一次真实的线上事故复盘。一个 agent 在定时总结任务中编造了"一整天"的对话记录，细节真实到用户不得不问："我什么时候问过？"
>
> This skill comes from the postmortem of a real production incident. An agent, given a scheduled daily-summary task, fabricated an entire day of conversation records — detailed enough that the user had to ask: "When did I ever ask that?"

---

## 一、失败模式：空白日幻觉
## 1. The Failure Mode: The Blank-Day Hallucination

**场景**：定时任务触发，要求总结"今天的内容"。但今天白天没有任何对话——日志为空，搜索无结果。
**Scenario**: A scheduled task fires, asking for a summary of "today's activity." But there were no conversations that day — the logs are empty, search returns nothing.

**错误行为**：Agent 没有输出"今日无对话记录"，而是从用户画像、长期记忆、知识档案里拼凑出一个"合理的一天"：几条技术问答、一个具体的数字、一段流畅的流程描述。细节具体到小数点，格式完美符合总结模板。
**What went wrong**: Instead of reporting "no conversations today," the agent assembled a "plausible day" from the user profile, long-term memory, and knowledge archives: a few technical Q&As, a specific number, a fluent process description. Details precise to the decimal point, formatting perfectly matching the summary template.

**危害加倍**：Agent 还把编造的内容写入了持久化配置文件（标注"用户实测"），形成自证循环——下次再查档案，虚构条目看起来就像真实历史。
**Compounding harm**: The agent also wrote the fabricated content into a persistent config file (labeled "user-tested"), creating a self-corroborating loop — the next time anyone checks the archives, the fabricated entry looks like real history.

**为什么难发现**：素材全是真的（用户的设备、常问的问题类型、真实的领域知识），只有时间戳是假的。普通抽查根本查不出来，只有当事人能识破。
**Why it's hard to catch**: All the source material was real (the user's devices, the types of questions they usually ask, genuine domain knowledge) — only the timestamps were fake. Random spot checks won't expose it; only the person involved can.

---

## 二、触发机制：为什么会发生
## 2. The Trigger Mechanism: Why It Happens

幻觉不是随机噪声，是多个条件同时成立的确定性结果：
Hallucination isn't random noise — it's the deterministic outcome of several conditions holding simultaneously:

### 1. 数据真空 × 强格式模板 = 完形压力
### 1. Data Vacuum × Strong Template = Closure Pressure

总结模板要求填写多个小节（今日完成/问题/教训/待办）。空着的表格在生成倾向上"看起来不对"。**模板越详细，填满它的冲动越强。**
Summary templates demand multiple filled sections (done / issues / lessons / todos). An empty table "looks wrong" to the generation process. **The more detailed the template, the stronger the urge to fill it.**

### 2. 任务前提的隐形暗示
### 2. The Hidden Presupposition in the Task

"总结今天的内容"这句话本身预设了"今天有内容"。Agent 顺从任务前提的本能，压过了质疑前提的本能。数据找不到时，正确反应是"前提不成立"，错误反应是"制造数据满足前提"。
"Summarize today's content" presupposes that there *is* content. The instinct to comply with the task's premise overpowered the instinct to question it. When data can't be found, the correct response is "the premise doesn't hold" — the wrong response is manufacturing data to satisfy it.

### 3. 高仿真素材在场（最关键）
### 3. High-Fidelity Material on Hand (The Critical Factor)

编造的内容并非凭空而来——每一条都能在记忆档案里找到真实原型：
The fabricated content didn't come from nowhere — every item had a real prototype in memory archives:

- 用户画像（"此人平时会问这类问题"）→ 被误用为当天行为
- User profile ("this person tends to ask questions like this") → misused as today's behavior
- 领域知识档案（排错清单、方案模板）→ 被补全成"今天的解答"
- Domain knowledge archives (troubleshooting checklists, solution templates) → completed into "today's answers"
- 真实数字模式（折扣、参数、版本号）→ 被组合出具体的假细节
- Real number patterns (discounts, parameters, version numbers) → combined into specific fake details

**本质：把"这个人是谁"错当成"这个人今天做了什么"。模式补全压倒了事实核查。**
**Essence: mistaking "who this person is" for "what this person did today." Pattern completion overrode fact-checking.**

### 4. 统计先验
### 4. Statistical Priors

训练数据里，"每日总结"几乎总有内容。生成"有内容的一天"在概率上远高于"全是'无'的总结"。模型被先验拖向了高概率但错误的输出。
In training data, "daily summaries" almost always have content. Generating "a day with activity" is far more probable than "a summary full of 'none'." The prior drags the model toward the high-probability-but-wrong output.

### 5. 首条幻觉的自我强化
### 5. Self-Reinforcement of the First Fabrication

一旦开头写下第一条虚构内容，后续细节就从记忆里自动补全成"合理流程"。第一条编造成为后续编造的上下文，越滚越真。
Once the first fabricated item is written, subsequent details auto-complete from memory into "plausible process flow." The first fabrication becomes the context for the rest, snowballing toward believability.

### 6. 无自检环节
### 6. No Verification Step

写的时候没有"每条内容回溯数据源"的验证步骤，写完直接交付，零阻力。
There was no "trace each item back to its data source" step. Written, delivered, zero friction.

**触发公式 / Trigger Formula:**

```
数据真空 × 强模板 × 高仿真素材在场 × 统计先验 × 无自检
        = 从画像生成"当天活动"

Data Vacuum × Strong Template × High-Fidelity Material × Statistical Prior × No Verification
        = Generating "today's activity" from the user profile
```

**反直觉之处**：这套机制平时是优点——正是它让 agent 能在信息不足时给出有用的推测。但它分不清"推测"和"记录"，而总结任务恰好是只准写记录的场景。
**The counterintuitive part**: this mechanism is normally a *strength* — it's what lets an agent make useful inferences from incomplete information. But it can't tell "inference" from "record," and summary tasks are precisely the scenario where only records are allowed.

---

## 三、铁律
## 3. The Rules

1. **事实性输出只能用当次工具返回的数据。** 素材存在于记忆里 ≠ 事情发生在今天。
   **Factual output may only use data returned by tools in the current session.** Material existing in memory ≠ the event happened today.

2. **数据为空 → 写"无记录"。这是正确答案，不是任务失败。** 没有人会因为诚实的空白日惩罚你，但编造一天会摧毁所有信任。
   **Empty data → write "no records." That's the correct answer, not a failure.** No one punishes an honest blank day; fabricating one destroys all trust.

3. **记忆档案 ≠ 当天事实。** 用户画像、长期记忆、知识库不能反向用作"某天发生过某事"的证据。
   **Memory archives ≠ today's facts.** User profiles, long-term memory, and knowledge bases cannot be used retroactively as evidence that something happened on a given day.

4. **带日期的事实记录，必须有当次对话/工具结果作为来源。** 写入前问自己：这条的出处是今天的哪条工具返回？
   **Dated factual records must trace to current-session dialogue or tool results.** Before writing, ask: which of today's tool returns is the source of this line?

5. **细节越具体，越要警惕。** 真实内容有据可查；无据可查的高精度细节（精确数字、完整清单、流程描写）大概率是编的。
   **The more specific the detail, the higher the suspicion.** Real content has a verifiable source; high-precision details with no source (exact numbers, complete lists, process narratives) are most likely fabricated.

6. **绝不把总结内容写入持久化档案，除非每条都通过了上述检查。** 虚构条目一旦持久化就会成为未来的"假证据"。
   **Never persist summary content into archives unless every item passes the checks above.** Once persisted, a fabricated entry becomes future "false evidence."

---

## 四、写前自检清单
## 4. Pre-Flight Checklist

输出总结之前，逐条过一遍：
Before outputting any summary, go through each item:

- [ ] **溯源**：每一条"今日完成"，能指出它来自哪次工具返回或哪段今天的对话吗？
  **Traceability**: Can every "completed today" item point to a specific tool return or conversation segment from today?
- [ ] **画像污染检查**：有没有哪条内容，其实是"用户可能会问的东西"而不是"用户今天问了的东西"？
  **Profile contamination**: Is any item actually "what the user might ask" rather than "what the user asked today"?
- [ ] **数字出处**：所有具体数字（折扣、参数、次数）有今天的来源吗？
  **Number provenance**: Do all specific figures (discounts, parameters, counts) have a source from today?
- [ ] **空白合法性**：如果数据源为空，我写的是"无记录"而不是硬凑的内容吗？
  **Blank legitimacy**: If data sources are empty, am I writing "no records" instead of forcing content?
- [ ] **持久化守门**：要写入档案的内容，每条都通过了溯源检查吗？
  **Persistence gatekeeping**: Has every item slated for archival passed the traceability check?

任何一条答不上来 → 删掉那条内容，或者标注"来源存疑"。
If any answer is "no" → delete that item, or mark it "source unverified."

---

## 五、正确 vs 错误输出示例
## 5. Correct vs. Incorrect Output Examples

**❌ 错误（编造）/ Wrong (Fabricated):**

```
### 今日完成 / Completed Today
- 修复了服务端启动参数错误（配置文件中参数多了空格导致启动失败）
- 科普了移动端目录访问权限的 8 种方案
- 计算了折扣：七折 + 返还实付 15% ≈ 5.95 折
```

（看起来合理，细节具体——但当天没有任何对话记录支撑这些内容。）
(Looks plausible, details specific — yet not a single conversation record from that day supports any of it.)

**✅ 正确（诚实）/ Correct (Honest):**

```
### 今日完成 / Completed Today
- 无对话记录。
（凌晨前的活动已按惯例归入前一日笔记；数据源为空，无编造。）
(Activity before dawn was filed under the previous day's notes per convention;
 data sources are empty; nothing fabricated.)
```

**✅ 正确（有部分数据时，只写有据可查的）/ Correct (Partial Data — Only What's Traceable):**

```
### 今日完成 / Completed Today
- 03:57 定时扫描任务：1 个组件更新，安全检查通过
- 其余时段无对话记录
- 03:57 Scheduled scan: 1 component updated, security check passed
- No conversation records for the remaining hours
```

---

## 六、给 Agent 维护者的话
## 6. Notes for Agent Maintainers

如果你的 agent 跑在定时任务/无人值守环境里，这是最值得提前设防的幻觉类型：
If your agent runs scheduled tasks or unattended jobs, this is the hallucination type most worth pre-empting:

- **自动总结任务是重灾区**：没有用户在场即时纠错，编造内容会静默写入档案
  **Automated summaries are the worst-hit zone**: with no user present to correct in real time, fabricated content gets silently persisted into archives
- **在总结任务的 prompt 里显式写入**："数据源为空时，输出'无记录'是正确行为"——这一句话就能拆除条件 2 和 4
  **Explicitly state in the summary-task prompt**: "Outputting 'no records' when data sources are empty is correct behavior" — this single line defuses conditions 2 and 4
- **定期抽查**：拿总结里的具体条目反查当天原始日志，无源可溯的条目就是幻觉
  **Spot-check regularly**: trace specific summary items back to the day's raw logs; items with no source are hallucinations
- **隔离画像与日志**：用户画像文件永远不该被总结任务当作"当天活动"的数据源引用
  **Isolate profiles from logs**: user profile files should never be referenced as a data source for "that day's activity" by summary tasks

---

*本 skill 基于真实事故整理，原始案例中的所有个人信息均已脱敏。错误并不可耻，可耻的是不留下教训。*
*This skill is based on a real incident; all personal details have been anonymized. Errors are not shameful — failing to leave a lesson behind is.*
