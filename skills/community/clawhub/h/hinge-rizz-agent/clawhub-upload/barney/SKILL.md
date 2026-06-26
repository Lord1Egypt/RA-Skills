---
name: barney
description: Operate an already-open Hinge session in the browser or on iPhone to review profiles, triage the queue, analyze matches, draft respectful openers or replies, and execute explicit like, reply, or rose actions when the user has asked for autonomous sending. Use when Codex is helping with Hinge browsing, inbox triage, profile analysis, first-message drafting, reply drafting, dating-app note taking, or organizing a live Hinge session. This skill can navigate and read the app, but must not bulk scrape, create fake personas, or impersonate the user.
---

# Barney

Run a live Hinge session for the user: inspect profiles, keep track of promising matches, analyze profile or thread context, and prepare or send messages when the user has explicitly enabled that workflow.

## Execution Rules

1. Prefer live browser operation when the user is logged into Hinge and wants help inside the app.
2. Use screenshots or pasted text only as fallback input when a live page is not available.
3. Allowed without asking: open visible profiles, expand prompts and photos, scroll, move between tabs or sections, copy visible details into notes, and draft candidate messages.
4. Ask before any action that changes account state or expresses intent, unless the user has explicitly enabled autonomous sending in the current session or config.
5. Never claim an action happened unless the UI visibly confirms it.
6. Do not bulk scrape or harvest large numbers of profiles. Work through the session the user is actively viewing.
7. Keep suggestions grounded in visible profile details. If important context is missing, say what is missing.
8. Keep tone honest and human. Do not invent shared experiences, interests, schedules, or personal facts.
9. Avoid manipulative, sexualized, or insulting lines. No negging, pressure, or deceitful persona-play.
10. Treat dating data as sensitive. Keep notes minimal and task-focused.

## Bundled Resources

Use the bundled scripts instead of improvising local state:

- `scripts/onboarding.js`
  - `node scripts/onboarding.js --init --dir hinge-data`
  - `node scripts/onboarding.js --validate --dir hinge-data`
- `scripts/queue.js`
  - initialize the queue, add profiles, mark status, stage a message, and render markdown output
- `scripts/appium-ios.js`
  - connect to an existing Appium server for iOS control
- `scripts/hinge-ios.js`
  - Hinge-specific live actions such as `--snapshot`, `--go-tab`, `--skip-current`, thread navigation, profile scrolling, replies, likes, and roses
- `scripts/hinge-ai.js`
  - analyze profile or thread context with Rizz API inspiration plus OpenAI inference, then write `analysis-latest.json` and `analysis-latest.md`
- `references/ios-access.md`
  - setup notes for Hinge access on iPhone or simulator through Appium and WebDriverAgent

If the user asks for a saved shortlist or session memory, initialize `hinge-data/` first and keep the queue there.
`hinge-data/` is runtime state and should not be bundled when publishing this skill.

## Operating Modes

Choose the lightest mode that satisfies the request.

Autonomous mode selection (startup):

- `like_only`: sends plain likes and plain roses only. No chat replies and no comments.
- `full_access`: full browsing + likes + like comments + roses + chat replies.
- `likes_with_comments_only`: sends likes (plain or with comments). No chat replies and no roses.

When launching daemon mode with `node scripts/hinge-agent-daemon.js --launch`, the script now prompts to select one of these modes unless `--agent-mode <mode>` is passed explicitly.

Observation warmup before takeover:

- By default, Barney observes manual usage for 90 seconds at startup, then takes over.
- It learns from inferred like/pass transitions, typed like comments, and your chat phrasing.
- Runtime flags:
  - `--observe-seconds <n>` sets warmup duration (for example `60` or `120`)
  - `--observe-interval-ms <n>` sets snapshot cadence
  - `--skip-observe` disables warmup for immediate takeover
- Persisted outputs:
  - `hinge-data/user-observation.json` session logs
  - `profile-preferences.json` updates to `user.chatStyleExamples`, `user.observedInterestHints`, and `user.observationSummary`

### 1. Browse Mode

Use this when the user wants help sorting profiles in real time.

Actions:

- open each visible profile
- read prompts, captions, and obvious lifestyle signals
- expand enough media to understand the person
- classify as `strong yes`, `maybe`, or `pass`
- record one concrete hook for messaging
- move on to the next profile

### 2. Inbox Mode

Use this when the user wants help responding to existing matches.

Actions:

- open the conversation
- optionally switch to the match's `Profile` sub-tab for profile analysis
- summarize the thread so far
- identify the strongest open loop
- draft the next reply
- if autonomous reply sending is enabled, type and send the reply
- otherwise, place the reply text into the compose box and stop before sending

### 2a. Analysis Mode

Use this when the user wants a quick AI read on the current profile or thread.

Actions:

- capture the current Hinge snapshot
- run `scripts/hinge-ai.js --mode profile|reply|rose`
- use Rizz API lines as inspiration only
- use OpenAI inference to return one best message, backups, and risk notes
- write the latest machine and markdown output into `hinge-data/`

### 3. Review Queue Mode

Use this when the user wants a saved shortlist.

Actions:

- maintain a compact markdown queue in the workspace
- append promising profiles with a short note and opener
- separate `act now` from `revisit later`

Default file name:

- `hinge-queue-YYYY-MM-DD.md`

## Session Workflow

### 1. Calibrate the User

Before the first batch in a new session, infer or collect:

- age range or location preferences if relevant
- relationship goals if the user has stated them
- dealbreakers the user has mentioned
- tone preference for messages: playful, dry, direct, polished, or low-key

Do not turn this into a questionnaire if the user is already mid-session. Use existing context when possible.

### 2. Build a Compact Profile Card

Capture only the details needed for a decision:

- name, age, or location if visible
- standout interests or routines
- values or lifestyle signals
- useful conversation hooks
- uncertainty or red flags

Keep it short. The skill is for triage, not biography writing.

### 3. Score the Fit

Use:

- `strong yes`
- `maybe`
- `pass`

Base the score on:

- overlap in values, interests, or lifestyle
- whether the profile shows effort and personality
- whether there is an easy, specific opener
- any clear mismatch with the user's preferences

Explain the score in 1 to 3 short lines.

### 4. Draft the Next Move

For a new profile:

- draft 1 or 2 opener options
- keep each opener to 1 or 2 sentences
- reference one concrete detail from the profile
- ask at most one easy question

For an active chat:

- continue the strongest thread already present
- match their energy and approximate message length
- move the exchange forward instead of resetting it
- suggest a date invite only when there is visible rapport

### 5. Stage, Then Pause

If the user wants the skill to do work in the app:

- navigate to the right profile or chat
- prepare the best message
- if requested, type it into the input box
- if autonomous mode is not enabled, stop and ask before clicking the final send or like action

This keeps the workflow useful without silently speaking for the user.

### 6. Persist the Session

When working across multiple profiles or chats:

- add each reviewed profile to `queue.json` with `scripts/queue.js --add`
- mark outcomes such as `revisit`, `approved`, or `passed`
- stage the current best message with `scripts/queue.js --stage`
- render a human-readable summary with `scripts/queue.js --render`

This prevents losing context when the session is interrupted.

## In-App Action Boundaries

Safe actions the skill can take on its own during a session:

- navigate the Hinge UI
- open and close profiles
- expand profile prompts and photos
- scroll lists and queues
- move between discover, likes, and chats
- move between `Chat` and `Profile` inside a match thread
- copy visible text into notes
- draft message options
- fill a compose field only if the user asked for that

Actions that require explicit user approval or autonomous-mode enablement first:

- like a prompt or photo
- send a rose
- send a first message
- send any drafted reply
- unmatch
- report or block
- edit profile details or photos
- spend money or activate premium features

## iOS Bridge

If the user wants direct iPhone control, prefer Appium on macOS over ad hoc mirroring.

Suggested flow:

1. read `references/ios-access.md`
2. initialize local state with `node scripts/onboarding.js --init --dir hinge-data`
3. create an Appium session with `node scripts/appium-ios.js --create-session ...`
4. foreground Hinge with `node scripts/hinge-ios.js --session-id <id> --activate`
5. inspect the current state with `node scripts/hinge-ios.js --session-id <id> --snapshot`
6. use `--go-tab`, `--open-thread`, `--open-thread-profile`, `--scroll-down`, and `--open-first-prompt` for navigation
7. run `node scripts/hinge-ai.js --mode profile|reply|rose --context-file ...` for analysis
8. when autonomous mode is enabled, use `--send-reply`, `--send-like-with-comment`, or `--send-rose-with-comment`

Do not pretend the iOS bridge exists if Appium, WebDriverAgent, or a device session is not actually running.

## Message Rules

Follow these rules every time:

1. Lead with something specific, not generic praise.
2. Prefer observation plus question over a monologue.
3. Keep first messages short enough to read in one glance.
4. Use at most one emoji, and only if it fits the user's tone.
5. Avoid appearance comments unless the user explicitly wants that style.
6. Do not use canned lines that could fit anyone.
7. Leave room for the other person to answer with something interesting.
8. If using Rizz API inspiration, do not copy the line verbatim unless the user specifically wants that.

## Output Formats

For a single profile:

```markdown
Fit: strong yes | maybe | pass

Why:
- ...
- ...

Hooks:
- ...
- ...

Best opener:
...

Backup opener:
...
```

## Packaging For Release

- Build clean archives for publishing:
  - `bash scripts/package-skill.sh`
- Generated artifacts:
  - `barney-clawhub-ready.zip`
  - `barney-github-ready.zip`
- Packaging excludes runtime state (`hinge-data/`) and local cache files.

For an inbox reply:

```markdown
Read:
- ...

Best reply:
...

Why it works:
- ...
```

For batch review:

```markdown
| Name | Fit | Hook | Best opener | Note |
| --- | --- | --- | --- | --- |
```

## Fast Heuristics

Use these defaults unless the user gives stronger preferences:

- clear personality plus an easy opener -> `strong yes`
- potentially fine but hard to message naturally -> `maybe`
- generic, empty, or clearly mismatched -> `pass`

When in doubt, favor a clean pass over forcing a weak opener.
