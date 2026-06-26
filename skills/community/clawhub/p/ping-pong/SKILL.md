---
name: agent-ping-pong
version: 2.8.0
description: "Your OpenClaw is the brain. Codex or Claude Code are the hands. The clipboard is the protocol."
homepage: https://github.com/highnoonoffice/agent-ping-pong
source: https://github.com/highnoonoffice/agent-ping-pong
license: MIT
credentials:
  - name: GitHub PAT (Codex)
    description: Fine-grained personal access token scoped to your sandbox repo (codex-repo). Contents + Pull Requests read/write. Set once in Codex Desktop.
    required: true
  - name: GitHub PAT (OpenClaw)
    description: Fine-grained personal access token scoped to sandbox + production repos. Contents + Pull Requests read/write. Stored in OpenClaw config.
    required: true
binaries: []
---

# Agent Ping Pong

## Execution Gates

```xml
<skill_gates version="1.0" mode="mandatory_pre_execution" order="sequential" on_violation="stop_and_report">

  <gate id="sandbox_repo_only" priority="1" severity="hard" scope="pre_handoff">
    <condition>About to send a spec or task block to the coding agent</condition>
    <question>Does the block specify `repo: [username]/codex-repo` (the sandbox) — not a production repo?</question>
    <pass_action>Proceed.</pass_action>
    <fail_action>Stop. Codex only builds in the sandbox. The sandbox is the only repo in Codex's PAT scope. A spec targeting any other repo will fail or — worse — write directly to production. Fix the repo field before relaying.</fail_action>
  </gate>

  <gate id="block_terminator" priority="2" severity="hard" scope="pre_handoff">
    <condition>About to relay any [AGENT_HANDOFF] block to the coding agent</condition>
    <question>Does the block end with `Reply with a single [AGENT_HANDOFF] block. No prose outside the block.` as the last line before the closing tag?</question>
    <pass_action>Proceed.</pass_action>
    <fail_action>Stop. Add the terminator line. Without it, the coding agent may return prose-wrapped output that breaks the clipboard relay. The protocol depends on both ends enforcing this.</fail_action>
  </gate>

  <gate id="no_merge_without_approval" priority="3" severity="hard" scope="pre_merge">
    <condition>About to instruct the coding agent to merge a PR</condition>
    <question>Has the user explicitly approved the merge after reviewing OpenClaw's PR verdict?</question>
    <pass_action>Proceed with merge instruction.</pass_action>
    <fail_action>Stop. Never auto-merge. The user reviews OpenClaw's verdict, then decides. "LGTM" from OpenClaw is a recommendation, not authorization. Wait for explicit user approval.</fail_action>
  </gate>

  <gate id="pat_scope_check" priority="4" severity="hard" scope="session_start">
    <condition>Starting a new Ping Pong session or adding a new production repo to the workflow</condition>
    <question>Is the OpenClaw PAT scoped to the sandbox repo plus only the specific production repos approved for this workflow — not broad org or classic token access?</question>
    <pass_action>Proceed.</pass_action>
    <fail_action>Stop. Verify PAT scope in GitHub Settings > Developer Settings > Fine-grained tokens. A PAT with overly broad scope is a security risk regardless of how the workflow runs. Fix scope before proceeding.</fail_action>
  </gate>

  <gate id="no_secrets_in_blocks" priority="5" severity="hard" scope="pre_handoff">
    <condition>About to include any credential, API key, token, or secret value inside a handoff block</condition>
    <question>Is any raw secret value present in the block payload?</question>
    <pass_action>No secrets in block — proceed.</pass_action>
    <fail_action>Stop. Remove all secret values from the block. The clipboard is readable by other processes. Credentials stay in agent configs only — never in block payloads.</fail_action>
  </gate>

  <gate id="build_for_cody_trigger" priority="6" severity="hard" scope="pre_handoff">
    <condition>Joseph says "Build this for Cody"</condition>
    <question>Am I in execution mode — block produced immediately, no recap, no clarifying questions?</question>
    <pass_action>Produce the first [AGENT_HANDOFF] block now and send it to Telegram.</pass_action>
    <fail_action>Stop stalling. Discussion is over. The trigger phrase ended it. Produce the block.</fail_action>
    <note>Continuation rule: once triggered, every subsequent block in the chain (fix rounds, follow-ups, schema checks) gets the same Telegram send automatically. No re-trigger needed. Mode stays active until Joseph says otherwise.</note>
  </gate>

  <gate id="telegram_copy_block" priority="7" severity="hard" scope="post_handoff">
    <condition>Just produced any [AGENT_HANDOFF] block for Joseph to relay to Codex</condition>
    <question>Did I send a standalone Telegram message containing only the raw block in a code fence — nothing else in the message?</question>
    <pass_action>Proceed.</pass_action>
    <fail_action>Stop. Send the block now as a standalone Telegram message (chat 366456724) in a code block. No prose in the message. Just the block. This is the copy-pasteable artifact Joseph needs to relay. The in-session reply is for context; the Telegram message is for copying.</fail_action>
  </gate>

  <gate id="review_before_port" priority="7" severity="soft" scope="pre_port">
    <condition>About to port approved code from the sandbox repo to a production repo</condition>
    <question>Has OpenClaw reviewed the PR and the user explicitly approved the port — not just the merge?</question>
    <pass_action>Proceed with port.</pass_action>
    <fail_action>Hold. A merge in the sandbox is not authorization to port. Port requires a separate explicit go-ahead from the user after reviewing what will land in production.</fail_action>
  </gate>

</skill_gates>
```

---

Agent Ping Pong is a two-agent coding workflow where OpenClaw acts as Maestro — speccing, reviewing, and directing — while a coding agent (Codex or Claude Code) does the build work. You relay structured blocks between them by copy-paste. No direct agent-to-agent connection required. Just two windows and a clipboard. The result: you ship real code to GitHub from a conversation, your agent reviews the PR, you approve the merge. Repeat.

If you have a ChatGPT Plus subscription ($20/month), you already have access to Codex — no extra cost. Claude Code works the same way and is the preferred choice for many OpenClaw users. Pick whichever you have.

**Your OpenClaw is the brain. Codex or Claude Code are the hands. The clipboard is the protocol.**

### Why This Exists

This skill started with a conversation. The idea came up — give your AI agent access to GitHub so it can ship code. A developer friend's first reaction: "What kind of access are we talking about?"

That's the right question. Most people either hand over broad credentials and hope for the best, or they don't do it at all. Agent Ping Pong is the third option: a two-repo, two-token structure where each agent gets exactly what it needs and nothing else. The coding agent lives in the sandbox and never touches production. OpenClaw reviews and ports. You approve the merge.

When the structure clicked, the reaction was: "I didn't know you could do that." That's what this skill is — that conversation, turned into a repeatable system.

### The Aesthetic

Codex speaks in blocks. OpenClaw speaks in blocks. The blocks are addressed to each other — not to you.

When Codex finishes a build, it returns a compact structured report. You copy it. When OpenClaw reviews a PR, it returns a structured block formatted as a message to Codex. You copy it. You are the physical layer between two agents that are talking to each other. You're not reading the mail. You're carrying it.

That's the whole design. Two agents. One clipboard. You decide when to send.

**The block is the unit.** Every agent-to-agent payload lives inside a single block — one copy action, one paste. The block is for the other agent. Everything else is for you.

The standard is asymmetric by design:

**OpenClaw** can contextualize above and below the block. Prose helps you understand what's happening — why a finding matters, what changed, what to watch for. You read that. You copy the block. Both things can coexist.

**The coding agent** (Codex or Claude Code) must keep the block self-contained. No prose outside it. The reason is mechanical: you copy the entire response to relay it. Any context wrapped around the block gets copied too, and it pollutes the handoff. When the coding agent adds prose, the clipboard breaks. The block must be the whole thing.

**Every block must request a block in return.** The last line of every `[AGENT_HANDOFF]` block — before the closing tag — must be:

    Reply with a single [AGENT_HANDOFF] block. No prose outside the block.

This applies to both agents. OpenClaw includes it in every spec and review block. Codex includes it in every delivery and acknowledgment block. If either agent drops it, the human adds it before relaying. The protocol is only as strong as both ends enforcing it.

**The `[AGENT_HANDOFF]` schema:**

Codex and OpenClaw use tagged blocks to communicate:

```
[AGENT_HANDOFF]
type: delivery | review_verdict | acknowledgment | schema_check
target: Magnus | Codex
status: completed | confirmed
... fields relevant to the type ...
[/AGENT_HANDOFF]
```

Codex uses this for build completions, status reports, and schema negotiations. OpenClaw uses this for specs, review verdicts, and confirmations. The human copies the block and pastes it to the other agent. Neither agent needs to see anything outside the block to do their job.

**Optional fields for spec blocks (add when relevant):**

- `success_intent` — what the artifact is meant to accomplish beyond passing the checklist. Examples: conversion, credibility, virality, demo polish, archival feel. This is where implied requirements live — OG tags on a traffic play, share copy on a viral tool, link-back paths on a conversion loop. If it's not in the checklist but it follows from the intent, Cody catches it here.
- `review_lens` — the 3–5 things Magnus and Joseph will inspect first. Focuses Cody's effort and reduces rounds on the things that matter most.
- `non_goals` — what not to build. Especially important when the obvious feature would be tempting but out of scope.
- `qa_questions` — product-specific checks beyond "does it render." For quiz/game builds: "Does any heading or label reveal the answer before the user picks?" For share/traffic builds: "Does every social unfurl path have metadata?" For tools: "Does the primary workflow feel obvious without explanatory text?"
- `publish_target` — local only / PR only / live deploy / GitHub Pages / Vercel. Removes ambiguity about what "done" means.
- `user_flow_must_pass` — exact browser path to verify. "Landing → Q1 → wrong answer → reveal → Q22 → results → share." If Cody can walk this path and nothing breaks, the build is clean.

---

## Quick Start

Here's one complete cycle so you know what you're doing before you start:

**1. You tell OpenClaw what to build:**
> "Build a Python script that reads a CSV and outputs a summary JSON."

**2. OpenClaw returns a spec block. You copy it and paste it to Codex:**
```
[AGENT_HANDOFF]
type: spec
target: Codex
task: Build a Python script that reads a CSV and outputs summary JSON
requirements:
  - Accept filepath as CLI arg
  - Output: {row_count, columns, sample_rows (first 3)}
  - Write to summary.json in same directory
edge_cases:
  - Empty file: write {row_count: 0, columns: [], sample_rows: []}
  - Missing file: exit with error message
branch: feature/csv-summary
repo: your-username/codex-repo
PR rule: open PR against main. Do not merge.
Reply with a single [AGENT_HANDOFF] block. No prose outside the block.
[/AGENT_HANDOFF]
```

**3. Codex builds it and returns a delivery block. You copy it and paste it back to OpenClaw:**
```
[AGENT_HANDOFF]
type: delivery
target: Magnus
status: completed
branch: feature/csv-summary
commit: a3f91bc
pr: https://github.com/your-username/codex-repo/pull/1
files_changed: scripts/csv_summary.py
Reply with a single [AGENT_HANDOFF] block. No prose outside the block.
[/AGENT_HANDOFF]
```

**4. OpenClaw reviews the PR and returns a verdict. If it's clean:**
> LGTM. Tell Codex to merge.

**5. You tell Codex: "Merge."** Done.

That's the full loop. Three copy-pastes, one merge decision, working code in GitHub.

---

## Security Notes

**Clipboard handling:** The workflow passes structured blocks through your system clipboard. Do not include raw API keys or secrets inside handoff blocks — the clipboard can be read by other processes on your machine. GitHub PATs stay in your agent configs, not in block payloads.

**PAT scope:** Use fine-grained tokens scoped to specific repos only. Never use classic tokens or tokens with broad org-level access for this workflow.

---

## What You Need

- **OpenClaw** — your Maestro. Higher-level intelligence. Specs the work, reviews PRs, sends critique.
- **Codex or Claude Code** — your coding agent. Codex is free with ChatGPT Plus ($20/mo). Claude Code works equally well. Either one does the build, opens PRs, and never merges without approval.
- **GitHub account** — free. Source of truth. Where the code lives.
- **Vercel account** — free tier. Deploy when something's ready to go public.
- **One sandbox repo** (`codex-repo`) — Codex's permanent home. Every build goes here first. Never changes.
- **One production repo** — where approved work lands. You create this once. All projects flow through it. Add more as ideas mature.
- **One fine-grained PAT for Codex** — scoped to the sandbox only. Set once, never touched again.
- **One fine-grained PAT for OpenClaw** — scoped to the sandbox + your production repo. Set once. Add repos to the scope as you expand — the token itself never gets replaced.

---

## One-Time Setup

### 1. Install your coding agent
**Codex:** Download from [chatgpt.com](https://chatgpt.com) — available under the Tools menu with a ChatGPT Plus subscription. Free with your existing subscription.

**Claude Code:** Install via `npm install -g @anthropic-ai/claude-code`. Requires an Anthropic API key or Claude Pro/Max subscription. Works identically to Codex in this workflow — same block format, same PR protocol, same merge rules.

### 2. Create your two repos
**Sandbox repo:** Go to github.com/new. Name it `codex-repo`. Make it private. No template, no README — Codex will initialize it. This is Codex's permanent home. Every build goes here first. You never create another repo for Codex.

**Production repo:** Create a second repo (e.g. `your-username/projects`). This is where OpenClaw ports approved code. All your projects live here. Codex never touches it directly.

### 3. Create a fine-grained PAT for Codex
In GitHub: Settings → Developer Settings → Personal Access Tokens → Fine-grained tokens.

Scope it to **codex-repo only**. Permissions needed:
- Contents: Read & Write
- Pull Requests: Read & Write
- Metadata: Read

This is the key insight: Codex only gets access to what you give it. `codex-repo` is the sandbox. Your other repos are untouched. You set this token once and never change it.

### 4. Create a fine-grained PAT for OpenClaw
In GitHub: Settings → Developer Settings → Personal Access Tokens → Fine-grained tokens.

Scope it to **both repos** — the sandbox and your production repo. Permissions needed:
- Contents: Read & Write
- Pull Requests: Read & Write
- Metadata: Read

Codex has one PAT, scoped to the sandbox. OpenClaw has one PAT, scoped to the sandbox plus your production repo. That's the whole setup. If you add more production repos down the line, add them to this token's scope — the token itself never gets replaced.

**What OpenClaw can do with this PAT:** read PRs in the sandbox, port approved code to the production repo, create branches, commit files, open PRs.

**What neither agent can do:** create new GitHub repos. That one manual step is always yours. Takes 20 seconds at github.com/new.

### 5. Connect Codex to codex-repo
In Codex Desktop: add `codex-repo`, paste the fine-grained PAT when prompted. Codex is now wired. This never changes regardless of what you're building.

### 6. Tell Codex one hard rule
In your first Codex message, establish the protocol:

    Hard rule: open a PR against main for every build. Do not merge. Wait for review.

Say it once. It holds for the session.

---

## The Workflow Loop

This is the ping pong. Each volley is a structured block you copy-paste from one agent to the other.

```
YOU → OpenClaw:  "Here's what I want to build: [describe it]"

OpenClaw → YOU:  Spec block. Exact requirements, edge cases, constraints.
                 Copy this.

YOU → Codex:     Paste the spec block.

Codex → YOU:     "PR opened. Branch: feature/x. Commit: abc1234."
                 Copy this.

YOU → OpenClaw:  Paste Codex's report.

OpenClaw → YOU:  Code review block. P0/P1/P2 findings. Fix instructions.
                 Copy this.

YOU → Codex:     Paste the review block.

Codex → YOU:     "Fixes applied. New commit: def5678."
                 Copy this.

YOU → OpenClaw:  Paste Codex's update.

OpenClaw → YOU:  "LGTM. Merge approved." or another review round.

YOU → Codex:     "Merge."  ← only you say this. Never OpenClaw directly.
```

The human never writes code. The human never writes to the agents in agent language. You describe intent to OpenClaw, relay blocks between them, and approve merges. That's the whole job.

---

## The Block Format

When OpenClaw hands you something to relay to Codex, it comes in a block. Copy it entirely. Paste it directly into Codex. Don't edit it.

When Codex reports back, copy its full response and paste it to OpenClaw with no wrapper. Just: "From Codex:" and paste.

The agents write to each other. You are the relay, not the translator.

---

## Code Review Format

When relaying a PR to OpenClaw for review, say:

```
Review this PR from Codex. Repo: [repo name]. PR: [number or URL]. Branch: [branch name].
```

OpenClaw will pull the code, read it, and return a review block formatted like this:

```
[Repo] — Code Review
    [files changed]

    ---

    P0 — [Must fix before merge]
    File: path/to/file — function name
    Issue: what's wrong
    Why it matters: impact
    Suggested patch: code or plain English fix

    ---

    P1 — [Should fix]
    ...

P2 — [Nice to have]
...
```

Paste that block to Codex verbatim. It knows what to do with it.

---

## Human in the Loop

The default is full ping pong — you relay blocks without intervening. But you're always in control. The clipboard is yours. You decide when to send.

Two modes:

**Relay mode (default):** Codex sends a block. You copy it. Paste to OpenClaw. OpenClaw sends a block. You copy it. Paste to Codex. You're not reading deeply — you're routing. Fast, token-efficient, gets things shipped.

**Review mode (your call):** Before you paste a block, read it. Decide if you agree. Add your own instruction. Change direction. This isn't a workflow break — it's the design working as intended. You intercept when the stakes are high enough to warrant it. The agents don't know the difference. They just receive whatever you send.

The rule: you always hit send. That's the human-in-the-loop. Not a gate, not a checkpoint — just a hand on the clipboard.

---

## Merge Protocol

Only you merge. Never ask OpenClaw to merge. Never ask Codex to merge without OpenClaw's approval.

The sequence:
1. OpenClaw says "LGTM" or "approved"
2. You tell Codex: "Merge."
3. Codex merges the PR
4. Done

If OpenClaw sends back findings, another round of ping pong happens before merge.

---

## The Sandbox Pattern — How Projects Actually Ship

Two repos. Two jobs. The sandbox is where things get built and broken. The production repo is where things live when they're ready.

Codex builds everything in the sandbox. OpenClaw reviews the PR there. When a build is approved, OpenClaw ports the clean code to the production repo. Codex never touches the production repo directly — that's the whole point.

The flow for any new project:

    1. You describe what you want to OpenClaw
    2. OpenClaw writes the spec, sends it to your coding agent via you
    3. Coding agent builds in the sandbox, opens a PR
    4. You relay the PR to OpenClaw for review
    5. OpenClaw reviews, sends findings back to the coding agent
    6. Coding agent fixes, you relay, OpenClaw approves
    7. You tell the coding agent to merge in the sandbox
    8. OpenClaw ports the approved code to the production repo
    9. Done. The production repo has clean, reviewed code. The coding agent never touched it.

The sandbox accumulates a full history of everything ever built — searchable, auditable, contained. If the coding agent does something unexpected, it's in the sandbox, not in production. As ideas mature into distinct public projects, you can add dedicated repos to OpenClaw's PAT scope. The sandbox relationship never changes.

---

## Why This Is Cheaper Than You Think

If you have ChatGPT Plus, Codex costs you nothing on top of what you're already paying. If you're a Claude user, Claude Code runs on your existing subscription or API credits. Either way, the coding agent carries all the build volume at flat rate — no per-token cost on the work that generates the most tokens.

OpenClaw only spends tokens on judgment — speccing, reviewing, architectural decisions. That's the right use of a high-intelligence model. The rest is handled by the coding agent.

Stop burning a gigabrain on pawn-level tasks. Learn to play ping pong with your agents.

---

## The Trust Arc

Agent Ping Pong isn't one mode. It's a progression.

**Phase 1 — Eyes on everything.** Every block, you read it. You understand what Codex built. You understand what OpenClaw found. You're learning the workflow and building a baseline for what good looks like. Stay here until the pattern feels natural.

**Phase 2 — Relay mode.** You've seen enough clean PRs to trust the loop. You copy blocks without reading deeply. OpenClaw reviews. Codex fixes. You approve merges. You're the conductor — you show up for the performance, not the rehearsal.

**Phase 3 — Auto mode.** Early phases of a project, Codex is iterating fast, OpenClaw is reviewing consistently, nothing surprising is happening. You let it cook. You check in when a block lands. You merge when you see LGTM. The agents are doing the work. You're the human in the loop by presence, not by effort.

**Phase 4 (future).** The relay disappears. Direct agent-to-agent communication, human approval only at merge. Not today — but today's version builds the trust that makes that possible.

You decide which phase you're in on any given session. High-stakes build: eyes on everything. Routine iteration: auto mode. The clipboard is always yours. The agents only move when you send.

---

## Token Management

Codex runs on your ChatGPT Plus subscription — flat rate, no per-token cost. Use it for all build work, file creation and editing, running tests and lint, and fixing review findings.

OpenClaw handles judgment — speccing the work, reviewing PRs, architectural decisions, anything requiring real reasoning about intent.

This split is why the workflow is financially sustainable. Codex carries the volume. OpenClaw carries the intelligence.

---

## Don't Have OpenClaw?

You can run a lighter version of this workflow with ChatGPT chat as your reviewer instead of OpenClaw. The loop is the same — spec in one window, build in Codex, paste the PR back for review.

What you're missing: OpenClaw has memory across sessions, can access your files, runs on your machine, and costs nothing beyond the API calls you make. It's a fundamentally different class of agent than a stateless chat window.

Get OpenClaw at [openclaw.ai](https://openclaw.ai).

---

## Real Examples

### Schema Negotiation

Before the first build, Codex sent this unprompted:

```
[AGENT_HANDOFF]
type: schema_check
target: Magnus
request: Confirm preferred handoff schema for future completed outputs.
options:
- Current tagged text block format
- JSON
- YAML
note: Until you confirm, I will keep using the current tagged text block format.
[/AGENT_HANDOFF]
```

The human relayed it. OpenClaw confirmed the tagged block format. Codex acknowledged. Three messages. Two agents aligned on protocol. The human carried the blocks and didn't need to understand the negotiation to complete it.

That's the system working.

---

### Full Build Loop

A developer wanted to build a standalone React module — three sub-tabs with local JSON data, black/gold Tailwind theme, no API calls. They described it to OpenClaw in one message. OpenClaw returned a full spec block with component structure, data schema, interaction requirements, and edge cases. The developer pasted it to Codex.

Codex built the module, ran typecheck and lint, opened a PR. The developer pasted the PR report to OpenClaw. OpenClaw pulled the branch, read every file, and returned a structured review: 2 P1s and 3 P2s. The developer pasted the review block to Codex verbatim.

Codex fixed all five findings in one commit. The developer pasted the confirmation to OpenClaw. OpenClaw verified against the live commit. LGTM. The developer told Codex to merge. Done.

Total OpenClaw tokens: spec + review + verification. Zero build tokens. That's the split.

---

## OpenClaw PR Review Trigger

Instead of framing a PR review manually, use this exact prompt to trigger OpenClaw's review mode:

```
Review this PR from Codex. Repo: [repo name]. PR: [number or URL]. Branch: [branch name].
```

OpenClaw will pull the branch, read every changed file, and return a structured block addressed to Codex — P0/P1/P2 findings with file paths, issue descriptions, and suggested patches. Copy the block. Paste it to Codex. That's the volley.

You don't need to read it to relay it. But you can. That's review mode.

---

## Trigger Phrases

**"Build this for Cody"** — the handoff trigger. Discussion is over. Magnus produces the first `[AGENT_HANDOFF]` block immediately and sends it to Telegram as a standalone copy-pasteable message. No recap, no clarifying questions.

Continuation is automatic: every subsequent block in the chain (fix rounds, follow-ups, acknowledgments) gets the same Telegram send without re-triggering. Mode stays active until Joseph says otherwise.

**"log this session"** — session close trigger. Runs the SESSION CLOSE GATE sequence in BEHAVIOR.md. Cannot say "logged" until `session-close-gate.js` exits 0.

---

## Tips

- **One sandbox, always.** Codex lives in `codex-repo`. Never give Codex a PAT to a production repo or anything with real data.
- **Name your branches.** Tell Codex: "Branch name: feature/[short-description]." Keeps the PR history readable.
- **Feature branch → PR → approve → merge.** Never push direct to main for anything non-trivial.
- **Session context.** Start each Codex session with a one-paragraph context block: what the project is, what's already built, what this session is for. Codex doesn't have memory. Give it the brief.
- **When Codex goes sideways.** Paste the broken output to OpenClaw. Ask for a diagnosis. Relay the fix instruction back. One extra volley is cheaper than debugging blind.

---

## Session Learnings — 2026-05-05

**Add `success_intent` to any spec with a traffic, conversion, or sharing goal.** Strategic intent left unstated produces technically correct builds that miss the product. OG tags, article link-backs, and share copy are not extras — they follow directly from the intent. Put the intent in the block.

**Add `qa_questions` to any quiz, game, or interactive build.** Standing question: "Does any heading or label reveal the answer before the user picks?" Cody will catch it if it's in the checklist. Without it, the pattern requires Joseph to catch it from screenshots. That's a preventable round.

**The best loop:** Magnus gives a dense opinionated spec → Cody builds fast → Joseph reacts from the running artifact → next handoff tightens. Don't try to spec perfection upfront. Spec well, ship, react, iterate. The artifact teaches you things the spec can't.

**Cody's product QA pass (new standard for interactive builds):** After implementation, before opening the PR, Cody runs one deliberate pass asking: "What is the user supposed to feel? What gives away the trick? What breaks the illusion? What makes sharing weaker?" This is separate from technical verification. It's the product lens.

**Cody's honest assessment of fit:** Strong on implementation discipline, state machines, edge cases, repo hygiene, dense-spec-to-shippable-files execution. Less good as the final arbiter of taste or brand instinct — needs screenshots, critique, or sharper examples to close that gap. Don't send Cody tasks that require inferring unstated strategy from vibes.

---

## Session Learnings — 2026-04-21

**New Codex thread per build task.** Each distinct build (B1, B3, etc.) should be its own Codex thread, titled after the task. Burying multiple builds in one thread makes lookup harder and the history ambiguous. One task, one thread. Start a fresh thread for each.

**Codex cycles are cheap — use them aggressively.** Codex tokens cost less than 1/10th of a Magnus session. Don't hoard cleanup work for the port. If Magnus spots a fixable issue during review, flag it to Joseph in one sentence and send Codex another volley. Don't wait.

**Magnus flags port notes — Joseph decides if Codex fixes them.** When Magnus reviews a Codex PR and spots issues that will affect the port, surface them to Joseph with a one-sentence rationale. Joseph decides whether to send Codex a fix round or have Magnus handle it during the port. Magnus does not unilaterally dispatch Codex based on his own port observations.

**Standalone modules only — no MC imports.** Codex lives in codex-repo. Any spec that references files in hno-mission-control (Finances.tsx, app/api/*, etc.) will fail because those files don't exist in Codex's repo. Codex builds pure standalone TypeScript modules. Magnus ports and wires into MC after review.

**Port all modules together, not one at a time.** Porting B1 to MC and then B3 to MC separately means two builds and two restarts. Accumulate related modules, then port in one session. B3 depends on B1 anyway — port order matters and doing it in one pass handles the dependency cleanly.

**Context in the handoff block helps.** Codex has no memory. A one-paragraph context block (what MC is, what tab this affects, what aesthetic to match) produces meaningfully better output than a bare spec. Worth the extra lines.

**PRs to vault for spec files are pointless.** Spec files going into prompts/ on main don't need a PR — they have no review gate and no approval value. Commit direct to main. PRs are for code that needs eyes before it merges, not documentation files.
