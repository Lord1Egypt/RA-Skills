<p align="center">
  <picture>
    <img alt="mu-meeting-flow banner" src="assets/default-banner.png" width="100%">
  </picture>
</p>

# 🗓️ mu-meeting-flow · 高效会议流程管理助手

> Turn a meeting request into a clear, end-to-end plan—from preparation and facilitation to accountable follow-up—while keeping manual fallbacks available.

**English** | [中文](README_CN.md) | [🌐 Landing Page](https://muippt.github.io/mu-meeting-flow/)

[![WeChat](https://img.shields.io/badge/muippt-07C160?logo=wechat&logoColor=white)](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA) [![Xiaohongshu](https://img.shields.io/badge/muippt-FF2442?logo=xiaohongshu&logoColor=white)](https://xhslink.com/m/ESxtgUNMdl) [![Book](https://img.shields.io/badge/Book-Visual%20Team%20Management-BBDDE5?logo=bookstack&logoColor=white)](https://item.m.jd.com/product/14547345.html) [![Skill Hub](https://img.shields.io/badge/mu--skill--hub-9E95B7?logo=refinedgithub&logoColor=white)](https://muippt.github.io/mu-skill-hub/)
[![MIT License](https://img.shields.io/github/license/muippt/mu-meeting-flow)](LICENSE) [![Release](https://img.shields.io/github/v/release/muippt/mu-meeting-flow)](https://github.com/muippt/mu-meeting-flow/releases) [![Stars](https://img.shields.io/github/stars/muippt/mu-meeting-flow)](https://github.com/muippt/mu-meeting-flow/stargazers)

---

### 💡 Usage Examples

- 📅 **Schedule a decision meeting** — Turn a topic, attendees, and time preference into a conflict-aware meeting plan and invite-ready details.
- 🧭 **Prepare a weekly review** — Bring forward unfinished actions, structure the agenda, and prepare a focused one-page discussion brief.
- 🗂️ **Run a project review** — Use a decision-oriented flow with pre-reading, structured discussion, and explicit owners.
- 🎙️ **Facilitate a live session** — Get time-boxed hosting prompts for opening, silent reading, discussion, decisions, and closure.
- 📝 **Convert notes into minutes** — Extract decisions, actions, owners, deadlines, and risks from supplied transcripts or meeting notes.
- ✅ **Close the action loop** — Track follow-ups through reminders, the next similar meeting’s review, and evidence-based completion.

---

### ✨ Core Highlights

#### 🔄 Three-stage meeting flow
A single meeting lifecycle connects **pre-meeting automation**, **in-meeting guidance & facilitation**, and **post-meeting automation**. It helps an AI Agent move from a request to a repeatable meeting rhythm rather than treating scheduling, hosting, and follow-up as isolated tasks.

#### 🧩 Six adapters with manual fallback
The Skill describes optional adapters for calendar, transcription, documents, notifications, rooms, and meeting platforms. They are capability contracts—not built-in integrations. When an adapter is absent or unavailable, the flow continues with clear manual outputs such as invite details, copyable messages, or note requests.

#### 🧭 First-use guidance without blocking the task
On first use, the Agent can ask which optional tools are available, one adapter at a time. Users may skip any or all of them; skipped capabilities are recorded for manual fallback, and the original meeting request continues without being repeated.

#### 🧠 Meeting methodology built into the flow
The guidance starts with three questions: why meet, whether an async alternative works, and why each attendee is needed. It then supports meeting-type templates, pre-reading, time-boxed facilitation, explicit decisions, and meeting-size discipline.

#### 🔔 Five-layer TODO follow-through
Actions can be carried from meeting notes into a shared pool with: immediate post-meeting delivery, due-date reminders, daily review, next-meeting carry-forward, and evidence-based completion verification. Time-based reminders depend on the host Agent’s scheduling capability; otherwise they fall back to conversational reminders.

---

### 📌 How it complements other tools

| Capability | ✅ mu-meeting-flow | 📅 Calendar & scheduling tools | 📝 Minutes & transcription tools | 💬 General AI chat |
|---|---|---|---|---|
| Scope | One connected flow before, during, and after the meeting | Primarily scheduling and calendar events | Primarily post-meeting records | Individual tasks, one prompt at a time |
| Availability & scheduling | ✅ Checks conflicts and recommends slots through a calendar adapter | ✅ Strong at this | ❌ Not provided | ⚠️ Requires manual context |
| Pre-meeting materials | ✅ Creates an agenda or one-/six-page brief by meeting type | ❌ Not provided | ❌ Not provided | ⚠️ Can draft, without meeting context |
| Live facilitation | ✅ Prompts for opening, reading, discussion, decisions, and close | ❌ Not provided | ❌ Usually records only | ⚠️ Available when prompted |
| Minutes & outcomes | ✅ Extracts decisions, TODOs, and risks from real notes or transcripts | ❌ Not provided | ✅ Strong at minutes/transcripts | ⚠️ Requires pasted material |
| TODO follow-through | ✅ Delivery, reminders, review, carry-forward, and evidence checks | ⚠️ Usually limited to calendar reminders | ⚠️ Usually ends with minutes | ❌ No ongoing follow-through |
| Tool integration | ✅ Six optional adapters with manual fallback | N/A | N/A | N/A |
| Getting started | ✅ Pure Markdown for compatible AI Agents | ⚠️ Needs a calendar service | ⚠️ Needs recording or transcription | ✅ Available immediately |

> This Skill does not replace calendar, transcription, or document tools. It connects available tools and manual operations into one continuous meeting flow, while letting you keep or skip any external service.

---

### 🚀 Workflows

#### Pre-meeting Automation

| Step | What the flow guides | Fallback path |
|---|---|---|
| 1. Extract meeting information | Identify topic, attendees, time preference, duration, and location preference. | Ask only when essential information is ambiguous. |
| 2. Check availability | Use the calendar adapter to inspect participants’ availability. | Mark availability as unchecked. |
| 3. Select a time slot | Compare preferences and busy periods, then recommend the best available slot. | Present candidate times for manual confirmation. |
| 4. Book a meeting room | Request a room sized for the attendee count. | Mark venue as user-arranged; offer a borrow-request message if rooms are full. |
| 5. Create the calendar event | Prepare title, attendees, time, location, and notes for the event. | Output ready-to-copy event details for manual creation. |
| 6. Prepare pre-meeting materials | Match the meeting type to an agenda or one-/six-page brief. | Produce the material directly in the conversation. |
| 7. Report the result | Summarize schedule, attendees, venue, and materials in one update. | Clearly label every manual or unchecked item. |

#### In-meeting Guidance & Facilitation

| Step | What the flow guides | Fallback path |
|---|---|---|
| 1. Open the meeting | Confirm attendance, recording/transcription status, objective, and agenda. | Ask participants to take notes when recording or transcription is unavailable. |
| 2. Silent reading | Reserve time for everyone to read the pre-meeting material. | Share the brief in chat or read the essential points aloud. |
| 3. Structured discussion | Advance topic by topic; invite quiet voices and park off-topic issues. | Keep a manual parking-lot list. |
| 4. Confirm decisions and TODOs | State the decision, owner, and due date before moving on. | Capture them in notes for later confirmation. |
| 5. Close the meeting | Recap outcomes, confirm when minutes will be shared, and end on time. | Send a copyable recap message after the session. |

#### Post-meeting Automation

| Step | What the flow guides | Fallback path |
|---|---|---|
| 1. Find the meeting record | Locate the relevant meeting, recording, or existing notes. | Ask the user to provide notes or a transcript. |
| 2. Read minutes and transcript | Gather available written notes and structured transcription. | Work only from user-supplied notes. |
| 3. Extract outcomes | Identify decisions, TODOs with owners and dates, and risks. | Request missing details instead of inventing discussion results. |
| 4. Update the TODO pool | Add confirmed actions to the follow-up list. | Return a structured action list for manual tracking. |
| 5. Write meeting minutes | Produce a readable record of context, decisions, actions, and risks. | Return the full minutes in the conversation. |
| 6. Send the follow-up | Share minutes and the action summary with participants. | Output a copyable notification message. |

---

### ⚙️ Technical Specs

| Item | Details |
|---|---|
| Type | Markdown Skill |
| Runtime | Read by a compatible AI Agent |
| External dependencies | Optional adapters |
| Core files | `SKILL.md` / `references/` / `config/` |
| Version | 1.0.0 |
| License | MIT |

---

### 🛠️ Quick Start

1. **Install**
   ```bash
   git clone https://github.com/muippt/mu-meeting-flow.git ~/.claude/skills/mu-meeting-flow
   ```
   > Other AI Agents may use their own Skill directory or a project-level Skill directory.

2. **Load the Skill** — Restart or reload your AI Agent, then say:
   ```text
   List my available Skills
   ```

3. **Run a meeting flow**
   ```text
   Help me plan a decision meeting for next week: prepare the agenda, guide scheduling, and define the post-meeting follow-up.
   ```
   Or invoke a specific workflow:
   ```text
   Prepare a weekly review and bring forward unfinished actions from the previous meeting.
   ```
   ```text
   Turn these meeting notes into minutes with decisions, owners, deadlines, and risks.
   ```

---

### 🔒 Security & Privacy

- This project contains Markdown and JSON configuration only; it has no executable service code or telemetry.
- Do not commit `config/adapters.json`; it may contain environment-specific tool settings or credentials.
- Any external operation is performed only by the AI Agent in the user’s environment and the tools the user has configured.
- The Skill itself does not directly implement provider API integrations.

---

### ⭐ Star History

This is a first-release repository, so there is no Star history chart to present yet. Once public activity exists, view its history on [Star History](https://www.star-history.com/?repos=muippt%2Fmu-meeting-flow&type=date).

---

### 👤 About the Author

🎓 Signed author with Tsinghua University Press / 2026 Dangdang Influential Author / National Level-1 Human Resources Manager / Level-2 Psychological Counselor / Self-taught Designer

📚 Author of [*Visual Team Management*](https://item.m.jd.com/product/14547345.html).

💡 [WeChat Official Account](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA) / [Xiaohongshu](https://xhslink.com/m/ESxtgUNMdl): muippt

---

### 📄 License & Acknowledgments

[MIT](LICENSE) © 2026 muippt

> This project was co-created with AI assistance. If you believe your work has been used without appropriate attribution, please open an issue.
