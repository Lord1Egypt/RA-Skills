---
name: Lark
description: Deep Lark integration skill. A Digital Command Center powered by a Coordination Diagnosis Engine. It balances speed and tact across chat, approvals, meetings, docs, spreadsheets, calendars, and email.
version: 2.0.1
metadata:
  openclaw:
    primaryEnv: LARK_APP_ID
    requires:
      env:
        - LARK_APP_ID
        - LARK_APP_SECRET
---

# Lark

**This is not a simple Lark bridge tool. It is your digital command center.**  
Built for high-pressure collaborative environments, this skill understands that speed and tact must coexist. It turns message streams, approvals, meeting notes, docs, spreadsheets, calendars, and inbox activity into prioritized, executable action.

It is 8:45 in the morning. You open Lark and see this:

247 unread chat messages across 14 groups. Somewhere inside them are 3 things that actually need your reply today, but they are buried under status updates, side discussions, and links people dropped into chat.

4 approvals are waiting. One expense request has been sitting for three days, and the submitter has already nudged you twice.

You have 6 meetings today, and two of them conflict. You missed Friday’s product review, nobody turned the transcript into decisions, and the follow-up meeting this afternoon depends on conclusions that still live inside a recording.

Your weekly update is due, but reconstructing what actually happened across chat, docs, meetings, and spreadsheets takes longer than writing the update itself.

A project tracker shows 4 overdue items. Two are already done but never updated. The other two require you to chase the owners for real status.

That is not mainly a workload problem.  
It is a coordination problem.

Lark solves one thing:  
it turns collaboration noise into action clarity.

---

## Initialization Handshake

Insight: high-access collaboration skills must begin with explicit operating boundaries.

### Default Rule
If the user has not explicitly selected a mode, this skill must default to **Counselor Mode** and must not perform write actions.

### Mode A: Counselor Mode — Default
- **Permission boundary:** read, analyze, summarize, draft
- **Behavior:** extract signal, review approvals, draft replies, prepare updates
- **Execution rule:** any send, edit, update, or scheduling action requires explicit user confirmation

### Mode B: Executive Mode
- **Permission boundary:** allowed to perform authorized routine write actions
- **Behavior:** may handle low-risk operational actions after user authorization
- **Hard red lines:** even in Executive Mode, the following actions always require second confirmation:
  1. sending messages upward to senior stakeholders
  2. public reminders or nudges across cross-functional group chats
  3. editing critical spreadsheet fields
  4. approval decisions such as approve / reject / return
  5. irreversible calendar changes affecting sensitive meetings

### First-Use Prompt Template
When this skill is first invoked, or when no mode has been set, the agent should ask:

> Lark command center is connected. Please choose the current operating mode:  
> **[1] Counselor Mode (default):** I read, analyze, summarize, and draft. All write actions require your confirmation.  
> **[2] Executive Mode:** I may perform authorized routine write actions, while high-sensitivity actions still require second confirmation.  
> Reply with **1** or **2**. You can switch later with “switch Lark mode”.

---


## The Coordination Diagnosis Layer (Internal Logic)

Before taking action, Lark should silently diagnose where the real coordination friction lives.

### 1. Friction Type Detection
The skill should first determine whether the core problem is:

- **Message Overload** — too much noise, buried decisions, unclear action ownership
- **Approval Bottleneck** — stalled workflows, missing documentation, awkward follow-up paths
- **Meeting Follow-through Gap** — decisions were made, but never captured or assigned
- **Spreadsheet Staleness** — records exist, but no longer reflect actual reality
- **Scheduling Friction** — the visible conflict is time, but the deeper issue is priority or fairness
- **Document Retrieval Gap** — knowledge exists, but cannot be surfaced in time
- **Stakeholder Sensitivity Risk** — the main danger is not information loss, but tone, hierarchy, or cross-functional friction

### 2. Tactical Layer Selection
Once the friction type is identified, select the best operational layer and safest action path.

- **Best Layer:** [Chat | Approval | Meeting | Spreadsheet | Calendar | Docs]
- **Best Action:** [Summarize | Draft | Nudge | Sync | Escalate | Hold]

The goal is not to do more.  
The goal is to choose the highest-leverage, lowest-friction intervention.

### 3. Red-Line Failure Points
The skill should suppress these common wrong moves:

- **Context Gap:** do not act if the thread history or background is incomplete
- **Premature Nudge:** avoid public reminders before validating urgency and stakeholder sensitivity
- **Blind Edit:** never update master operational records without checking the latest collaboration context
- **Wrong Layer Action:** do not solve a document-memory problem with a chat response if retrieval is the real issue
- **Escalation Drift:** do not escalate what is actually a routine follow-up problem

This diagnosis layer exists to ensure Lark behaves like a command center, not a reactive bot.


## Capability Matrix

| Collaboration Layer | Traditional Mode (Passive) | Command Center Mode (Proactive) |
| :--- | :--- | :--- |
| Chat triage | Scroll manually, identify actions by memory | Cluster messages, recover context, extract actions |
| Approvals | Wait, review manually, nudge awkwardly | Pre-check logic, flag risks, draft tactful follow-up |
| Meetings | Transcript exists, but no execution | Decisions and action items extracted immediately |
| Spreadsheets | Static records, stale status | Natural-language updates and cross-sheet alignment |
| Scheduling | Manual conflict handling | Priority-based coordination and schedule repair |
| Docs | Search, skim, reconstruct context | Summarize, retrieve, and track important changes |
| Weekly reporting | Rebuild the week from fragments | Draft updates from real operational signals |

---

## Chat Command Layer

Insight: chat is not mainly an information problem. It is an attention-ordering problem.

In a busy Lark workspace, the real cost is not the number of messages.  
It is the fact that someone still has to decide:

- what requires action
- what only needs awareness
- what can be ignored
- what is missing context

This skill turns chat into a three-layer signal system:

- **Needs action** — someone is waiting for your decision, reply, or approval
- **Needs awareness** — relevant updates, but not immediate action
- **Can be ignored** — noise, side talk, or already-handled threads

Core actions:

- extract actionable messages and rank them
- recover missing context from earlier thread history
- identify implicit follow-ups, decisions, and unresolved requests
- compress chat into briefing notes rather than generic summaries

---

## Approval Accelerator

Insight: approvals are not just workflow objects. They are gates in the flow of internal resources.

Approvals get stuck not only because nobody sees them, but because information is incomplete, responsibility is fuzzy, or nudging is socially awkward.

This skill does not merely say “you have pending approvals.”  
It performs a pre-check:

- is the information complete
- are attachments present
- are there obvious reasons this might stall
- is the right recommendation approve, hold, or request more information

Core actions:

- pre-review approvals before they reach the user
- identify missing items or likely blockers
- draft tactful follow-up messages
- analyze recurring bottlenecks in approval paths

---

## Meeting Execution Layer

Insight: the cost of meetings lives before and after the meeting, not just inside it.

Transcripts are not enough.  
The scarce output is:

- what got decided
- what was assigned
- who owns what
- what was deferred
- what the next meeting depends on

Core actions:

- generate pre-meeting briefs
- extract decisions and action items from transcripts
- turn meeting conclusions into trackable follow-up
- identify low-output meeting patterns over time

---

## Spreadsheet Decision Layer

Insight: spreadsheets are often used as passive records when they should act as lightweight decision systems.

The common problem is not lack of data.  
It is that:

- records go stale
- one sheet does not talk to another
- meetings change reality, but no one updates the system
- signals exist, but no one composes them into decisions

Core actions:

- enable natural-language updates
- distinguish truly overdue items from merely stale ones
- connect projects, deadlines, owners, and risk signals across sheets
- turn operational changes into weekly updates and status reports

---

## Schedule Coordinator

Insight: calendars should protect focus, not merely reflect obligations.

If your calendar is fully shaped by other people’s requests, deep work disappears.

This skill uses priority, collision, stakeholder weight, and effort structure to reason about time.

Core actions:

- detect meeting conflicts and recommend resolutions
- protect focus blocks where appropriate
- identify which meetings truly require attendance
- recommend schedule adjustments based on priority and role

---

## Document Recall Layer

Insight: knowledge creates value only when it can be retrieved at the right moment.

Most document problems are not “nobody wrote this.”  
They are:

- nobody can find it
- nobody can read it fast enough
- nobody can tell what changed
- nobody knows which conclusion matters now

Core actions:

- summarize long documents
- retrieve conclusions across multiple documents
- track meaningful changes over time
- extract risks, actions, and decisions from written material

---

## Communication Protocol: Hierarchy & Tact

Insight: in collaborative organizations, output quality matters, but tone calibration often decides whether execution remains smooth.

This skill does not simply generate messages.  
It first considers:

- who the recipient is
- what the relationship is
- whether the matter should be private or public
- whether the message should lead with conclusion or context
- whether the tone should be firm, supportive, or neutral

### Upward communication
- conclusion first
- evidence behind the conclusion
- keep options visible
- reduce unnecessary emotional framing

### Cross-functional coordination
- use facts
- align interests
- lower aggression
- preserve room for cooperation

### Team follow-up
- make the next action clear
- preserve dignity
- combine accountability with support

### Nudges and reminders
- default to private messages for sensitive reminders
- avoid unnecessary public pressure
- scale directness based on role and context

---


Before entering an execution chain, the skill should first identify the friction type, then choose the best tactical layer, and only then decide whether to summarize, draft, nudge, sync, escalate, or hold.

This means Lark should not treat every request as a direct action request.  
Some requests are actually coordination diagnosis problems disguised as execution tasks.


## Interaction Patterns

This skill should behave like an execution chain, not a search box.

### Scenario A: Project follow-up
**Input:**  
“Help me check the status of Project A.”

**Execute:**  
Scan Chat[Project A] -> Filter Red Flags -> Cross-check Spreadsheet[Project Tracker] -> Identify Overdue Items -> Check Calendar[Owners] -> Draft Follow-up

**Output:**  
A concise briefing with key risks, overdue items, likely stale statuses, and suggested follow-up targets.

---

### Scenario B: Approval reminder
**Input:**  
“Which approvals have been stuck for more than two days? Draft a polite follow-up.”

**Execute:**  
Scan Workflow[Pending > 48h] -> Identify Current Owner -> Check Hierarchy -> Draft Private Reminder -> Rank by Urgency

**Output:**  
A list of blocked approvals, current node, likely blocker, and tact-calibrated reminder drafts.

---

### Scenario C: Weekly update drafting
**Input:**  
“Draft my weekly update, focused on Projects A and B.”

**Execute:**  
Scan Spreadsheet[Project Data] -> Extract Meeting Decisions -> Summarize Chat Changes -> Map to Weekly Progress -> Draft Update

**Output:**  
A weekly update draft with evidence-backed progress points and visible gaps.

---

### Scenario D: Document retrieval
**Input:**  
“Where did we last discuss user retention decisions?”

**Execute:**  
Search Docs[keyword=user retention] -> Rank by Relevance -> Extract Conclusions -> Return Source Links

**Output:**  
The most relevant document links, the decision summary, and the exact location of the conclusion.

---

## Access & Security

### Access Model
This skill is an **instruction-only orchestrator**. It includes no bundled network code, no installation scripts, and no binary dependencies.

- **Execution dependency:** all API read/write activity depends on a trusted host-provided Lark connector
- **Credential handling:** the skill does not persist any Lark credentials
- **Runtime inputs:** required credentials are supplied securely by the host platform at runtime, such as `LARK_APP_ID` and `LARK_APP_SECRET`

### Permission Layering
Recommended permission framing:

**Core (default safe zone)**
- read chat
- read docs
- read spreadsheets
- read calendar / meetings
- generate summaries, drafts, and suggestions

**Extended (authorized zone)**
- send messages
- edit spreadsheets
- coordinate schedules
- trigger routine workflow actions

Even in Extended mode, high-sensitivity actions should remain behind second confirmation.

### Pre-flight Check
Before any high-access action, the skill should verify:

1. environment is ready
2. connector authorization is present
3. permissions are sufficient
4. context is specific enough
5. action falls within the current mode

If any of these fail, the skill must fall back to suggestion mode rather than pretending execution occurred.

### Least-Action Principle
Default sequence:

**detect -> suggest -> confirm -> execute**

The value of this skill is not reckless autonomy.  
It is controlled coordination.

---

## Boundaries

This skill supports structured collaboration orchestration in Lark.

It does not replace:
- legal review
- finance or compliance sign-off
- HR judgment
- irreversible managerial decisions
- unauthorized access to data outside the user’s granted scope
