---
name: multi-ai-local-memory
description: Connect supported AI models, agents, and clients to one user-owned local shared memory through Multi-AI Local Memory. Default local memory app is Obsidian and default intermediary is OpenClaw, but neither is required.
homepage: https://github.com/a7904282000/multi-ai-local-memory
user-invocable: true
---

# Multi-AI Local Memory

Use this skill when the user wants multiple AI models, web/desktop clients, agents, or intermediaries to share one local memory.

## Required outcome

All connected endpoints MUST use one user-owned local `memory_space`:

- multiple models may read and write the same memory;
- web, desktop, agent, and intermediary surfaces must not create separate memory silos;
- local memory software is bidirectional whenever its adapter permits it;
- Obsidian is the default memory app, not a hard dependency;
- OpenClaw is the default intermediary, not a hard dependency.

## Memory rules

Do NOT store every conversation as long-term memory.

Prefer durable information such as:

- stable preferences;
- explicit remember requests;
- durable rules/instructions;
- confirmed decisions;
- project state and milestones;
- important long-lived facts.

Drop low-value filler, acknowledgements, test noise, and one-off wording.

Sensitive information is explicit-only. Secrets such as passwords, API keys, private keys, and reusable tokens MUST NOT become long-term memory.

## Source preservation

When importing or migrating existing memories, preserve the source exactly.

Required invariants:

- source bytes preserved 100%;
- source file count preserved 100%;
- source SHA-256 matches 100%;
- source relative paths preserved;
- originals are never silently rewritten, summarized, merged, normalized, or replaced.

Semantic indexes and normalized views are derived data only. They must be deletable and rebuildable from the authoritative source.

## Shared-memory behavior

The desired behavior is:

1. before an AI turn, recall relevant memory from the local shared memory;
2. inject only relevant recalled context;
3. after the final response, capture only durable new information;
4. write through the Local Bridge to the shared local memory;
5. synchronize changes to other supported local-memory peers;
6. preserve transaction identity, idempotency, provenance, and conflicts;
7. prevent recalled memory echoed by the model from being re-captured as new evidence.

Model/provider/client/agent/intermediary/device are provenance or authorization dimensions only. They MUST NOT partition memory.

## Native provider memory

Provider-private native memory is separate from the local shared memory.

If the provider exposes an official read/write memory interface, a provider-memory adapter may synchronize it.

If no official interface exists, do not claim the provider's private memory was modified. Provide shared-memory behavior via local recall before the turn and local capture after the turn.

## Installation / setup

Canonical project and runtime releases:

https://github.com/a7904282000/multi-ai-local-memory

Public Beta release:

https://github.com/a7904282000/multi-ai-local-memory/releases/tag/v1.0.0-beta.1

The Local Bridge/runtime is distributed separately from this ClawHub Skill. This Skill MUST NOT pretend that installing the Skill alone gives a web page direct access to local files.

When local execution is available, guide the user to install the Local Bridge/runtime from the canonical GitHub release and then use the runtime's zero-config install path.

If the current surface cannot execute on the user's machine, say that local installation is blocked on that surface and give the exact required user action. Do not claim installation succeeded without runtime evidence.

Browser security confirmations such as "Add extension" may remain as unavoidable external approvals. Token copy, extension-ID copy, manual sync, manual memory-space setup, and routine JSON/YAML editing are not acceptable normal-user setup steps.

## Completion gate

Do not call deployment complete until the user's environment demonstrates:

- local bridge healthy;
- one shared memory space;
- automatic credential provisioning;
- model A -> model B memory recall;
- model -> local memory software write;
- local memory software -> model update;
- bidirectional synchronization;
- restart recovery;
- duplicate durable writes = 0;
- original source archive intact;
- no routine manual memory sync.

For Public Beta, live website/provider compatibility may be validated by the user after installation. Keep user acceptance simple: one AI writes a test memory, another AI recalls it, the user changes it in the local memory app, and an AI recalls the updated value.

## Failure handling

Use evidence priority:

`Raw Runtime > Contract/Protocol > Verifier/Test > UI`

Use only these status labels:

`PASS / FAIL / UNPROVEN / BLOCKED`

Do not reopen a locked PASS boundary without new raw regression evidence.

Do not use progressive blind repair. Build the full failure boundary first, then fix the confirmed structural cause and scan same-class risks.
