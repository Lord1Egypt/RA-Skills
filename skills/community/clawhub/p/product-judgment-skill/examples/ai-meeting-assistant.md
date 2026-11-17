# 示例：AI会议纪要助手 / Example: AI Meeting Summary Assistant

**判决 / Verdict: VALIDATE FIRST / 先验证**

---

## 输入需求 / Input Demand

> 我们想做一个AI会议纪要助手，自动录音、转录、总结会议内容，并生成带责任人的待办事项清单。
> We want to build an AI meeting assistant that auto-records, transcribes, summarizes meetings, and generates a to-do list with assigned owners.

---

## Strike 1: 病灶命名 / Disease Diagnosis

**病型 / Pattern: Demo成瘾症 + 替换成本失明 / Demo Addiction Syndrome + Replacement Cost Blindness**

这个需求在演示时非常好看——AI转录、自动总结、智能分配待办——每项能力单独拿出来都令人印象深刻。
This demand looks great in demos — AI transcription, auto-summary, smart task assignment — each capability is impressive on its own.

但真实动机是：团队有语音转文字 + 大模型总结能力，想找一个"有用"的包装场景。
But the real driver is: the team has speech-to-text + LLM summarization capability and is looking for a useful packaging scenario.

这不是从用户的真实痛点出发，而是从技术能力出发反推场景。
This is not starting from a real user pain point — it's working backward from technical capability to find a use case.

---

## Strike 2: 假设审讯 / Assumption Interrogation

**需求成立，需要以下假设全部为真：**
**This demand requires ALL of the following to be true:**

| # | 假设 / Assumption | 验证状态 / Status |
|---|-----------------|-----------------|
| 1 | 用户参加的会议足够高频，值得专门安装工具 / Users attend meetings frequently enough to justify a dedicated tool | ❌ 未验证 / Unverified |
| 2 | 用户愿意在会议中开启录音（法律/隐私/心理障碍）/ Users are willing to record meetings (legal/privacy/psychological barriers) | ❌ 未验证 / Unverified |
| 3 | AI生成的纪要质量足够高，用户愿意直接使用 / AI-generated summaries are high enough quality for direct use | ❌ 未验证 / Unverified |
| 4 | AI分配的待办准确，不需要大量人工校对 / AI-assigned tasks are accurate enough to avoid manual correction | ❌ 未验证 / Unverified |
| 5 | 待办能在现有任务系统中被执行跟踪 / To-dos can be tracked in the user's existing task management system | ❌ 未验证 / Unverified |
| 6 | 与会者愿意接受AI分配给他们的任务 / Meeting participants accept AI-assigned tasks | ❌ 未验证 / Unverified |

**已验证 / Verified:** 无 / None

**当前证据等级 / Current Evidence Level:** L0 — 纯内部判断 / Pure internal opinion

**用户价值公式 / User Value Formula:**

| 维度 / Dimension | 内容 / Content |
|----------------|---------------|
| 旧体验 / Old Experience | 手动记录或不记录，会后靠记忆或微信群追踪 / Manual notes or no notes, relying on memory or group chat after meetings |
| 新体验 / New Experience | 自动转录 + AI总结 + 结构化待办 / Auto-transcription + AI summary + structured to-dos |
| 替换成本 / Replacement Cost | 录音授权（高）、学习新工具（中）、同事配合（高）、信任AI输出（高）、与现有任务系统集成（高）/ Recording consent (high), learning new tool (medium), colleague cooperation (high), trusting AI output (high), integration with existing task tools (high) |
| 净用户价值 / Net User Value | 未成立 / Not established — 新体验收益真实，但替换成本被严重低估 / New experience gains are real, but replacement costs are severely underestimated |

---

## Strike 3: 失败预演 / Failure Forecast

**第1个月 / Month 1:**
内部Demo非常顺利，领导觉得"AI感"很强，立项通过。
Internal demo goes smoothly. Leadership feels the "AI vibe." Project approved.

**第2-3个月 / Month 2-3:**
开始内测。发现很多公司不允许第三方软件录音。另一批用户开录音后，参会者明显沉默，会议质量下降。
Internal testing begins. Discovery: many companies prohibit third-party recording software. When recording starts, participants go noticeably quiet, meeting quality drops.

**第4个月 / Month 4:**
找到愿意用的用户群，但AI总结质量参差不齐——专业术语、项目名称、人名频繁出错，用户每次都要校对，"还不如自己记"。
A willing user group is found, but AI summary quality is inconsistent — technical terms, project names, and people's names frequently wrong. Users spend time correcting. "Easier to take notes myself."

**第5个月 / Month 5:**
待办功能上线，但与飞书/Jira/钉钉无法打通，待办只存在产品里，没有进入实际工作流。
To-do feature ships, but can't integrate with Feishu/Jira/DingTalk. To-dos live in the product only, never entering real workflows.

**第6个月 / Month 6:**
日活持续下降，团队开始讨论"是不是要加更多功能"。复杂度上升，核心问题仍然未解决。
DAU keeps declining. Team starts discussing "maybe we need more features." Complexity rises, core problem still unsolved.

**根因 / Root Cause:**
不是功能不够，而是替换成本中的"组织阻力"和"信任成本"从一开始就没有被认真评估。这类产品不是个人工具，是组织级工具，任何一个环节断掉都失败。
Not insufficient features — the "organizational resistance" and "trust cost" components of replacement cost were never seriously assessed. This is not a personal tool; it's an organizational tool. Any broken link in the chain causes failure.

---

## 建议 / Recommendation

**不要直接开发完整产品。先验证两个关键假设：**
**Do not build the full product. First validate two critical assumptions:**

**假设A — 录音接受度 / Assumption A — Recording Acceptance:**
找10家目标企业，直接问IT管理员和员工：你们允许第三方软件在会议中录音吗？
Ask IT admins and employees at 10 target companies: do you allow third-party software to record meetings?

成功标准 / Success criteria: 超过60%愿意 / More than 60% willing
失败信号 / Failure signal: 超过50%拒绝，需要重大方向调整 / More than 50% refuse — major pivot needed

**假设B — AI输出质量 / Assumption B — AI Output Quality:**
不做产品，先做人工模拟。用现成工具（讯飞/Whisper）转录5个真实用户的3次真实会议，用LLM手动整理总结和待办，发给用户，问：这个质量你愿意付费吗？愿意改变习惯吗？
Don't build — simulate manually first. Use existing tools (iFlytek/Whisper) to transcribe 3 real meetings for 5 real users, use an LLM to manually prepare summaries and to-dos, send to users, ask: would you pay for this quality? Would you change your habits?

两个假设都通过，再考虑立项。任何一个未通过，回来重新定义需求范围。
Both assumptions must pass before proceeding. If either fails, return and redefine the scope.
