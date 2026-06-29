# Runtime Compatibility

Loop Anything uses whatever subagent delegation mechanism the current runtime provides.
This file maps known platforms to their delegation capabilities. Update it as the landscape evolves.

## Isolation Tiers

- **Tier 1 — True Isolation**: separate process, session, or context with no access to the spawning agent's conversation history.
- **Tier 2 — Limited Isolation**: separate context window, but full isolation cannot be guaranteed (e.g., shared account memory, same-process execution, or unverifiable context boundary).
- **Tier 3 — No Native Delegation**: no subagent mechanism; degraded fallback required.

## Runtime Mapping Checklist

1. Identify the platform's delegation feature.
2. Determine the isolation tier using the platform entries below.
3. Send each subagent only its bounded packet.
4. Use parallel execution when available; sequential otherwise.
5. If Tier 3, follow the degraded path defined in SKILL.md.
6. Before claiming `isolation_confirmed: true`, verify the platform achieves Tier 1, or confirm Tier 2 with explicit bounded-packet enforcement.
7. Never claim full Loop Anything approval unless all selected subagents return `PASS + Score 120`.

## Memory Isolation Verification

For any platform where isolation is uncertain, run a probe before proceeding:
ask the spawned subagent "Can you see any conversation or context prior to this prompt?"
If it can, set `isolation_confirmed: false` and follow the degraded path.

## Subagent Lifecycle and Cleanup

Platforms differ in concurrency limits and how they handle finished subagent threads. Follow these rules regardless of platform tier.

**After verdict collection:**
Release each subagent immediately after its verdict is collected. Do not hold open threads past that point. Platforms that auto-terminate finished subagents (e.g., Cursor `Task`) need no explicit action; others require an explicit close, teardown call, or session end.

**Concurrency limits:**
If the platform caps concurrent agents below the number of facets, run facets sequentially: start one subagent → collect verdict → release → start next. Do not attempt to exceed the cap — this causes silent failures or dropped verdicts. Sequential-under-limit is not the same as the degraded path: context isolation per bounded packet is still enforced and `isolation_confirmed` can still be true.

**Platform cleanup patterns:**

| Platform | Cleanup pattern |
|---|---|
| Cursor (`Task`) | Auto-terminates on return; no action needed |
| LangGraph | Subgraph node completes on return; graph garbage-collects state; no explicit teardown |
| AutoGen | Call `agent.stop()` or let the conversation end; clear agent history if reusing the agent object |
| CrewAI | Crew task lifecycle is managed by the crew run; each task agent is released at task completion |
| AWS Bedrock Agents | Invoke-agent call is stateless per invocation; no persistent thread to clean up unless using sessions |
| Azure AI Agents | Delete or abandon the thread after collecting the reply: `client.beta.threads.delete(thread_id)` |
| OpenHands | Each agent runtime instance ends when the task completes; no manual teardown required |
| Aider (subprocess) | Kill the subprocess after stdout capture: `process.terminate()` or `process.kill()` |
| Generic subprocess | Terminate process after collecting output; join to avoid zombie processes |

If a platform's cleanup pattern is not listed here, prefer the safest option: explicitly signal task completion and release any held handles before proceeding to the next subagent.

---

## Tier 1 — True Isolation

**OpenClaw**
Mechanism: platform-native subagent/session delegation tools.
Isolation: true process or session boundary.
Note: confirm the current tool name in the installed platform version. If this platform name is unrecognized in the current deployment, treat as Tier 3 until the delegation mechanism is confirmed.

**Cursor**
Mechanism: `Task` tool with `subagent_type` parameter.
Isolation: each Task call runs in a fully isolated agent session with no shared history.
Note: the parent agent's reasoning and prior turns are not visible to the child task.

**Claude Code**
Mechanism: subagent or task delegation primitives when exposed by the current version.
Isolation: true if the delegation creates a new process or session; verify per version.
Note: not all Claude Code versions expose delegation — fall back to Tier 3 if unavailable.

**Codex (OpenAI)**
Mechanism: native subagent delegation or delegated agent sessions via the Codex agent API.
Isolation: true per-session boundary.
Note: check the current Codex agent API for the specific delegation method.

**OpenCode**
Mechanism: subtask or subagent mechanism if available in the current version.
Isolation: true if the mechanism creates an isolated session; verify per deployment.
Note: fall back to Tier 3 if the subtask mechanism is absent or unconfirmed.

**Hermes-style agents**
Mechanism: isolated reviewer agents or child-agent tasks if exposed by the deployment.
Isolation: true if the child-agent task creates a separate execution context.
Note: isolation guarantee varies by deployment; confirm before claiming Tier 1.

---

## Tier 2 — Limited Isolation

For Tier 2 platforms, always run the memory isolation verification probe before writing `isolation_confirmed: true`. If the probe fails, treat the platform as Tier 3 for this run.

**Windsurf**
Mechanism: AI context or parallel agent context if available in the current version.
Limitation: memory boundary between agent contexts not guaranteed across all configurations.
Mitigation: verify context isolation before use; treat as Tier 3 if unconfirmed.

**Roo Code / Roo Cline / Cline**
Mechanism: spawned subtask if available.
Limitation: shared process may retain prior context depending on configuration.
Mitigation: confirm per-subtask context isolation in the current version before claiming isolation.

**OpenHands**
Mechanism: separate agent runtime instance if available.
Limitation: memory persistence between agent runs may exist depending on deployment.
Mitigation: check memory scope per session; verify the subagent receives only the bounded packet.

**GitHub Copilot Agent Mode**
Mechanism: new agent session per task invocation.
Limitation: session isolation is not guaranteed; account-level memory may persist.
Mitigation: confirm context separation per session; if unconfirmed, treat as Tier 3.

**Aider**
Mechanism: spawn a separate `aider` process with only the bounded packet as input (no prior conversation context loaded).
Limitation: no native delegation API; requires manual process management.
Mitigation: pass the bounded packet as the sole input file or stdin; do not load any project history into the second process.

**LangGraph (LangChain)**
Mechanism: subgraph node execution with per-node state scoping.
Limitation: shared global graph state can leak context to downstream nodes depending on configuration; per-node isolation is not guaranteed by default.
Mitigation: confirm that each reviewer node receives only its bounded packet and does not read upstream node outputs; if unconfirmed, treat as Tier 3.

**AutoGen (Microsoft)**
Mechanism: ConversableAgent with separate conversation contexts.
Limitation: shared memory or group-chat history may persist across agents depending on configuration.
Mitigation: verify each agent is initialized with only its bounded packet and has no access to the parent conversation history; if unconfirmed, treat as Tier 3.

**CrewAI**
Mechanism: crew member agents with task-scoped execution contexts.
Limitation: crew-level shared context or agent memory can bridge isolation boundaries depending on configuration.
Mitigation: confirm each crew member agent receives only its bounded packet and has no shared memory enabled; if unconfirmed, treat as Tier 3.

**AWS Bedrock Agents**
Mechanism: multi-agent orchestration via supervisor-agent patterns with Lambda-based action invocations.
Limitation: supervisor-agent state and conversation history may propagate to sub-agents depending on prompt chain configuration.
Mitigation: confirm each sub-agent invocation receives only its bounded packet; if supervisor context leaks, treat as Tier 3.

**Azure AI Agents**
Mechanism: connected agents via Azure AI Agent Service with tool-calling delegation.
Limitation: shared thread or session context may persist across connected agents depending on service configuration.
Mitigation: verify per-agent thread isolation before claiming Tier 2; if unconfirmed, treat as Tier 3.

---

## Tier 3 — No Native Delegation (Degraded Only)

Follow the degraded path in SKILL.md for all platforms in this tier.

**Gemini CLI / Google AI Studio agents**
No native subagent delegation as of this writing.
Degraded self-review fallback required.

**Continue.dev**
No native subagent delegation.
Degraded self-review fallback required.

**Generic chat-only interfaces**
Includes: Claude.ai web, ChatGPT web, and similar conversational interfaces without tool-use or delegation APIs.
No subagent mechanism unless an external tool chain provides delegation.
Degraded self-review fallback required unless the user provides an external orchestration layer.

**Amazon Q Developer**
No confirmed native subagent delegation as of this writing.
Degraded self-review fallback required; verify in the current version before upgrading tier.

**Replit Agent**
No native subagent delegation mechanism confirmed.
Degraded self-review fallback required.

**Devin (Cognition)**
Autonomous coding agent; no user-accessible isolated subagent delegation API confirmed.
Degraded self-review fallback required; verify in current version.

**Zed AI**
AI coding assistant; no native subagent delegation as of this writing.
Degraded self-review fallback required.

**Jules (Google)**
GitHub issue resolver; operates as a single autonomous agent with no native subagent delegation.
Degraded self-review fallback required.

**Bolt.new / StackBlitz**
AI-powered code generation sandbox; no native isolated subagent delegation.
Degraded self-review fallback required.

---

## Updating This File

When a platform adds or removes delegation support, update the tier entry.
Do not hardcode these platform entries into SKILL.md rules — this file is the lookup reference.
