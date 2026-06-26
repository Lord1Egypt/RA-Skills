---
name: meeting-ops-router
description: Route meeting notes, transcripts, Feishu docs, wiki pages, or minutes links into concrete execution channels. Use when the user wants post-meeting follow-through, including extracting action items, assigning owners, writing back to Feishu docs, storing tasks in Bitable, sending follow-up messages, creating reminders, or delegating work to same-gateway OpenClaw sessions or sub-agents.
---

# Meeting Ops Router

Turn meeting content into an execution queue, then route each item to the right destination.

Do not stop at summary. The goal is to convert discussion into approved, trackable next steps.

## Core workflow

### 1. Ingest the meeting source
Accept:
- pasted notes or transcript
- Feishu doc link
- Feishu wiki link
- minutes link

If the source is in Feishu, read it first. Pull any linked transcript or follow-up document if available.

### 2. Extract an action queue
For every action item, capture:
- title
- owner
- due date, or `no explicit deadline`
- evidence, one short quote or rationale
- recommended route
- status, default `proposed`

Use `references/routing-rules.md` when route choice is ambiguous.

### 3. Route each item to one destination
Pick exactly one primary route per item:
- `feishu-doc`
- `feishu-bitable`
- `feishu-message`
- `reminder`
- `same-gateway-agent`
- `manual`

Prefer one clean route over spraying the same task everywhere.

### 4. Present a routing plan before execution
Show a compact table or numbered list with:
- item
- owner
- due
- route
- exact next step

Group by route so the user can approve in batches.

### 5. Execute only the approved items
After approval, perform the routed actions using first-class tools.

## Route selection rules

### feishu-doc
Use when the best next step is creating or updating a durable shared artifact.
Examples:
- action list write-back
- follow-up memo
- interview brief
- candidate summary

Use `feishu_doc`.

### feishu-bitable
Use when the meeting produces a repeatable task queue that should be tracked as rows.
Examples:
- recruiting pipeline follow-ups
- multi-owner action tracker
- weekly ops backlog

Use Bitable tools when the table exists or the user wants a structured tracker.
If no table exists yet, ask whether to create one or write to doc first.

### feishu-message
Use when the next step is notifying a person or group.
Examples:
- send recap
- ask for confirmation
- forward JD
- request feedback

Prefer the `message` tool if the gateway already has Feishu messaging configured. If target identity is unclear, draft the message instead of pretending it was sent.

### reminder
Use when the action is time-based follow-through.
Examples:
- remind me Friday to check candidate progress
- follow up with vendor next week

Use `cron` with reminder text that reads naturally when it fires.

### same-gateway-agent
Use when the item requires more agent work rather than simple delivery.
Examples:
- research competitor compensation bands
- rewrite JD into outreach copy
- review a linked document and return a recommendation
- turn notes into a polished memo

Use one of these:
- `sessions_spawn` for isolated delegated work
- `sessions_send` to a known session when continuing an existing workflow

Delegation message must include:
- source meeting context in 2 to 5 bullets
- the exact requested output
- deadline or urgency
- where to report back

### manual
Use when the step requires human judgment, authority, or sensitive negotiation.
Examples:
- final pricing decision
- legal approval
- compensation policy exception

## Execution mappings

Typical mappings:
- write action items back to the source doc -> `feishu_doc.append` or `feishu_doc.insert`
- create a tracker -> `feishu_bitable_create_app`, `feishu_bitable_create_field`, `feishu_bitable_create_record`
- send a message -> `message`
- create a reminder -> `cron`
- delegate deeper work -> `sessions_spawn` or `sessions_send`

Prefer the smallest reliable action. If direct execution is blocked, generate the next-best artifact:
- drafted message
- doc section ready to paste
- Bitable schema proposal
- delegated task brief

## Approval policy

Never silently send external messages or create a large number of records.

Good approval prompts:
- "I can route 1 and 2 to Feishu doc, 3 to reminder, and 4 to a sub-agent. Proceed?"
- "Reply with route batches, for example: doc 1 2, reminder 3, agent 4"
- "Say 'all' to execute every proposed route"

## Output shape

### Routing Plan
1. [Title]  
   Owner: ...  
   Due: ...  
   Route: ...  
   Next step: ...  
   Evidence: ...

### Ready now
- grouped by route

### Needs your choice
- items with missing destination, unclear owner, or missing table/chat target

### Manual
- items that should remain with the user

## Same-gateway delegation rules

When routing to another OpenClaw agent or session:
1. keep the delegated task narrow
2. include only relevant context from the meeting
3. state the output format explicitly
4. ask the sub-agent to return a concrete artifact, not a vague summary

Good delegated prompts:
- "Use the meeting context below to draft a recruiter outreach message for the IM role. Return a polished Feishu-ready message in Chinese and English."
- "Research current compensation range for junior-to-mid full-stack candidates with overseas background in Beijing/Singapore startups. Return a short benchmark memo."

## What not to do
- Do not return a long meeting summary before the routing plan
- Do not route the same item to multiple channels unless the user explicitly asks
- Do not fabricate message targets, Bitable ids, or session names
- Do not mark delegated work done before the delegated session reports back
