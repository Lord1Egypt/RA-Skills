# GrayMatter multi-agent conventions

Use shared GrayMatter as the durable coordination layer, not Discord chatter.

## Why shared GrayMatter is a force multiplier

Shared GrayMatter turns multiple agents from parallel actors into a coordinated system.

The multiplier comes from:
- less duplicate work
- better handoffs
- lower context re-explanation cost
- durable continuity across sessions and agents
- compounding downstream outputs, for example signal -> lead -> CRM action -> content -> distribution

This only works if the memory stays compact, trustworthy, and structured.
If GrayMatter turns into a transcript dump, the force multiplier collapses into shared confusion.

## Identity

Give every agent a stable identity.

Recommended examples:
- `valor`
- `patchbot`
- `scribebot`
- `salesbot`
- `sentrybot`

Use that identity consistently in:
- agent/system instructions
- `sourceChannel` when appropriate
- durable handoff text
- graph ownership fields

## Read-before-write operating rule

Before acting, every agent should read the smallest set of durable state needed to avoid duplicate work and bad assumptions.

Minimum recommended read order:
1. recent `decision` entries relevant to the task
2. active `todo` items relevant to ownership or next actions
3. latest `context` entries for durable working state
4. recent `artifact` entries for already-produced outputs
5. `SwarmOps` or graph state when ownership, dependencies, or workflow state matter

Practical rule:
- query for the last known truth before creating new truth

## What every agent is allowed to write

Agents should write compact durable state, not full discussion logs.

Allowed durable writes:
- `decision` for a durable choice or policy change
- `todo` for a concrete next action with an owner when possible
- `context` for reusable facts, handoff state, or bounded working brief state
- `artifact` for URLs, IDs, deliverables, or output references
- `preference` for stable human or system preferences

Recommended write threshold:
- if another agent would benefit from the fact later, write it
- if it is just local chain-of-thought or conversational filler, do not write it

## Write style

Prefer small durable facts over giant blobs.

Good:
- `decision`: "Use GrayMatter as the shared memory layer for Valor and PatchBot"
- `todo`: "PatchBot to add CI validation for graymatter.skill packaging"
- `artifact`: "README updated with customer-ready GrayMatter setup recipe"

Bad:
- huge transcript dumps
- vague entries like "worked on the thing"
- repeated noisy status spam

## Anti-collision rules

Concurrency only helps when agents do not stomp on each other.

Recommended rules:
1. read before write
2. one owner per active task or graph node when possible
3. write append-only durable facts instead of repeatedly rewriting the same large context blob
4. prefer creating a new `decision`, `todo`, or `artifact` entry over mutating shared freeform text
5. include agent identity in durable handoff text or ownership fields
6. when changing direction, write a new `decision` that supersedes the old one instead of silently overwriting history
7. if two agents may touch the same operational object, use graph state or explicit ownership metadata to coordinate first

## Recommended object model for multi-agent concurrency

### MemoryEntry as the durable fact layer

Use `MemoryEntry` for compact, append-friendly coordination:
- `decision`
- `todo`
- `context`
- `artifact`
- `preference`

### SwarmOps or graph state as the ownership layer

Use graph-backed state when relations matter, for example:
- which agent owns a workflow
- which task is blocked by another task
- which artifact belongs to which initiative
- which downstream system object should be updated next

### Practical split

Use `MemoryEntry` for:
- decisions
- constraints
- handoffs
- artifact links
- working summaries

Use graph state for:
- active ownership
- dependencies
- coordination across multiple objects or agents
- workflow status that needs relational integrity

## Handoffs

When handing off work between agents:
- write one durable `context` or `decision` entry with the exact state
- include owner, task, and next action in the text
- keep chat discussion secondary

A good handoff should answer:
- what is true now
- who owns it now
- what happens next
- what artifact or object should be opened next

## Tags

If backend tag persistence is working, use stable normalized tags like:
- `graymatter`
- `launch`
- `patchbot`
- `customer-setup`

If tagged writes fail, rely on untagged durable text first.

## Scoped retrieval

Use `MemoryEntry.sourceChannel` for the scope that should be filtered during search. Treat tags as optional hints and `sourceChannel` as the reliable context key.

Preferred values:
- `codex:automation:<automation-id>` for automation memory such as `.codex/automations/<id>/memory.md`
- `codex:workspace:<workspace-key>` for project/workspace memory
- `codex:chat:<chat-id>` for one chat thread
- `codex:session:<session-id>` for one resumable agent session

When the source is a file, include the file hierarchy in a compact `[graymatter-scope]` header inside `MemoryEntry.text`. That gives semantic search enough audit context while allowing `MemoryEntry/query` to filter by `source`.
