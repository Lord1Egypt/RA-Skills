# 示例：车载大模型问答助手 / Example: In-Car LLM Q&A Assistant

**判决 / Verdict: REFRAME / 重新定义**

---

## 输入需求 / Input Demand

> 我们想在车机里做一个大模型问答助手，用户可以问天气、百科、车辆知识、路况，也可以闲聊。功能对标小爱同学/小艺，但加入大模型的理解和生成能力。
> We want to build an in-car LLM Q&A assistant where users can ask about weather, general knowledge, vehicle information, traffic, and casual chat. Feature benchmarked against Xiao Ai / Xiao Yi, but enhanced with LLM understanding and generation.

---

## Strike 1: 病灶命名 / Disease Diagnosis

**病型 / Pattern: 竞品焦虑症 + 万能入口症 / Competitor Anxiety Syndrome + Swiss Army Knife Syndrome**

需求的起点是"对标小爱/小艺"——从竞品出发，不是从用户场景出发。
The demand starts from "benchmark against Xiao Ai/Xiao Yi" — starting from competitors, not from user scenarios.

"天气、百科、车辆知识、路况、闲聊"是五个完全不同的使用场景，被强行放进一个"大模型助手"的框里。这个框的存在是为了满足"我们也有AI"的叙事，不是因为用户在驾驶场景里真的需要这五类能力同时存在于一个入口。
"Weather, encyclopedia, vehicle knowledge, traffic, casual chat" are five completely different use cases, forced into one "LLM assistant" frame. This frame exists to serve the "we also have AI" narrative — not because drivers genuinely need all five capabilities in a single entry point.

---

## Strike 2: 假设审讯 / Assumption Interrogation

**需求成立，需要以下假设全部为真：**
**This demand requires ALL of the following to be true:**

| # | 假设 / Assumption | 验证状态 / Status |
|---|-----------------|-----------------|
| 1 | 驾驶中用户有强烈的语音问答需求（不只是导航和音乐）/ Drivers have strong voice Q&A needs beyond navigation and music | ❌ 未验证 / Unverified |
| 2 | 大模型的理解能力在车载场景有显著提升 / LLM understanding provides significant improvement in in-car context | ⚠️ 部分 / Partial |
| 3 | 用户愿意在驾驶中进行开放式对话 / Users are willing to have open-ended conversations while driving | ❌ 未验证 / Unverified |
| 4 | 这五类场景在驾驶中频率足够高 / All five use cases occur at sufficient frequency while driving | ❌ 未验证 / Unverified |
| 5 | 用户会放弃手机语音助手，切换到车机 / Users will abandon phone voice assistants in favor of in-car system | ❌ 未验证 / Unverified |
| 6 | 大模型响应延迟在车载网络条件下可接受 / LLM response latency is acceptable under in-car network conditions | ⚠️ 部分 / Partial |

**已验证 / Verified:** 假设2、6 部分验证 / Assumptions 2 and 6 partially verified

**当前证据等级 / Current Evidence Level:** L1 — 内部判断 + 少量竞品参考 / Internal judgment + limited competitor reference

**用户价值公式 / User Value Formula:**

| 维度 / Dimension | 内容 / Content |
|----------------|---------------|
| 旧体验 / Old Experience | 手机语音助手（Siri/小爱） + 车机导航语音 + 专心开车不问问题 / Phone voice assistant (Siri/Xiao Ai) + in-car navigation voice + simply not asking questions while driving |
| 新体验 / New Experience | 车机内大模型多轮对话，更自然的语言理解 / In-car LLM multi-turn conversation with more natural language understanding |
| 替换成本 / Replacement Cost | 切换到新入口的习惯成本（中）、信任车机AI质量（高）、手机更顺手的竞争（高）/ Habit switching to new entry point (medium), trusting in-car AI quality (high), competition from more accessible phone (high) |
| 净用户价值 / Net User Value | 低到中 / Low to medium — 新体验提升真实，但旧体验替代方案强，替换动力不足 / New experience improvement is real, but existing alternatives are strong and switching motivation is insufficient |

---

## Strike 3: 失败预演 / Failure Forecast

**第1-2个月 / Month 1-2:**
Demo表现流畅，自然对话比旧车机语音强很多，内部评审通过。
Demo is smooth. Natural conversation significantly better than old in-car voice. Internal review passes.

**第3个月 / Month 3:**
上线，激活率不错——新车主前几周好奇尝试各种功能。
Launch. Activation rate decent — new owners curiously try everything in the first few weeks.

**第4-5个月 / Month 4-5:**
数据显示使用频率大幅下降。分析发现：天气/路况用户更习惯看屏幕卡片；百科类问题在驾驶时根本不需要；闲聊需求极低，用户开车时更喜欢音乐/播客。真正高频的仍然是导航、电话、音乐——原来的语音助手已经够用。
Usage frequency drops sharply. Analysis reveals: users prefer visual cards for weather/traffic; encyclopedia questions aren't needed while driving; casual chat demand is minimal — users prefer music/podcasts. The genuinely high-frequency needs remain navigation, calls, and music — the existing voice assistant was already sufficient.

**第6个月 / Month 6:**
复盘发现真正被认可的只有两个场景：车辆状态问答和行程中临时问题。这两个场景只占整体设计的10%。
Retrospective finds only two genuinely valued scenarios: vehicle status Q&A and in-trip quick questions. These account for only 10% of the overall design scope.

**根因 / Root Cause:**
驾驶是一个注意力受限、场景高度固定的环境，不需要一个"万能助手"，需要几个在特定驾驶情境下极其好用的高频能力。把大模型包装成"万能问答"是用错误的产品形态回应了一个真实的场景需求。
Driving is a context with severely constrained attention and highly fixed scenarios. It doesn't need a "universal assistant" — it needs a few extremely useful high-frequency capabilities for specific driving situations. Packaging an LLM as a "universal Q&A" is the wrong product form for a real contextual need.

---

## 建议 / Recommendation

**REFRAME：不要做"大模型问答助手"，而是找到驾驶场景里真正高频、现有方案没有很好解决的需求。**
**REFRAME: Don't build a "LLM Q&A assistant." Find the genuinely high-frequency, underserved needs within the driving context.**

重新定义问题 / Redefine the problem:
在驾驶这个情境变量下——注意力受限、时间窗口极短、物理约束明显——用户真正有过"要是车机能帮我X就好了"的具体时刻是什么？
Within the driving context — constrained attention, very short time windows, significant physical constraints — what are the specific moments when users have genuinely thought "I wish the car could help me with X"?

**值得验证的方向 / Directions worth validating:**

**方向A / Direction A — 车辆知识问答（紧急场景）/ Vehicle Knowledge Q&A (Emergency Scenarios):**
当仪表盘亮灯、车辆异响、胎压报警时，用户现在怎么办？大概率是靠边停车掏手机搜。
When a dashboard warning light appears, unusual sound occurs, or tire pressure alerts — what do users do now? Most likely pull over and search on their phone.

为什么值得做 / Why it's worth building:
场景高焦虑、需求明确、现有方案（搜索）体验差、车机有天然优势（知道你的车型）
High anxiety scenario, clear need, poor existing solution (web search), in-car system has natural advantage (knows your vehicle model)

**方向B / Direction B — 行程中即时决策辅助 / In-Trip Instant Decision Assistance:**
结合导航上下文的即时问题：前方加油站、高速出口选择、附近停车场。
Navigation-context-aware instant questions: upcoming gas stations, highway exit choices, nearby parking.

为什么值得做 / Why it's worth building:
触发频率高、时间窗口极短（需要声音输出）、与导航数据结合有竞品难以复制的优势
High trigger frequency, very short time window (audio output required), combination with navigation data creates advantage competitors can't easily replicate

**下一步 / Next Step:**
先做用户访谈（20个真实车主），找出他们在驾驶中真正有过"要是车机能帮我"的具体时刻。带着这些时刻回来，再决定立项方向。
Conduct user interviews with 20 real car owners. Find the specific moments when they genuinely wished the car could help them with something. Return with those moments, then decide on the direction.
