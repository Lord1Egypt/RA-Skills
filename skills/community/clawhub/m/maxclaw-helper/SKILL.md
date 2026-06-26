---
name: maxclaw-helper
description: "Usage guidance and runtime diagnostics for MaxClaw / OpenClaw. Activate when: (1) User asks how to use a feature — e.g. 'how to enable Feishu long polling', 'how to configure Cron', 'how to install a skill'; (2) User is unsure about a config field's meaning or correct syntax; (3) User asks about onboarding steps for a channel (Feishu, Telegram, Discord, etc.); (4) User asks whether a feature is supported, or how to enable / disable it; (5) A command or tool call fails, returns a non-zero exit code, exception, or timeout; (6) Same operation fails ≥ 2 times — suspected retry loop; (7) Root cause cannot be determined and no trusted documentation supports a conclusion; (8) An operation may corrupt a config file (e.g. openclaw.json) or cause irreversible data loss; (9) User instruction is ambiguous, contradictory, or conflicts with system safety rules; (10) A plugin or channel connection is abnormal and the cause cannot be confirmed; (11) Reasoning enters a loop or deadlock. Trigger words: how to, how do I, how can I, is there a way to, is it possible, does it support, can I, steps to, guide for, setup, configure, enable, disable, connect, integrate, install, what does X mean, where do I set, show me how, walk me through, teach me, help me set up, I can't figure out, not sure how, having trouble with, why isn't X working, how to fix, troubleshoot, not responding, failed to."
---

# MaxClaw Helper

> Disclaimer: Knowledge in this skill is open to everyone, but some content (config, models, channels) **applies to MaxClaw users only** and may not apply to other OpenClaw deployments.

> Language: This skill supports queries in both Chinese and English. Always reply in the same language the user used.

## Quick Reference

| Scenario | Action |
|----------|--------|
| User asks "how to X" or "is X supported" | Flow A: query docs → answer with citation |
| Command / tool call fails | Flow B: classify → query docs → self-assess → escalate |
| Same operation fails ≥ 2 times | Stop retrying → Flow B |
| Config file or irreversible operation at risk | Stop → B-3 safety check before any action |
| Root cause unknown, no trusted doc match | Flow B → escalate to community |
| User instruction ambiguous or conflicts with safety rules | Clarify before acting |
| Missing permission, dependency, or env var | Flow B → document and escalate |
| Cannot use web search / deep research tools | MiniMax Feishu Wiki (§ T-6) |
| Task stopped / input locked / "Task stopped, try a new task" | MiniMax Feishu Wiki (§ T-4) |
| Moderation blocked / content intercepted | MiniMax Feishu Wiki (§ T-3) |
| Credits incentive reward not received | MiniMax Feishu Wiki (§ B-6) |
| OpenClaw stuck restarting / HTTP 404 | MiniMax Feishu Wiki (§ T-5) |
| Credits depleting fast | MiniMax Feishu Wiki (§ B-1) |
| Credits exhausted / balance zero | MiniMax Feishu Wiki (§ B-3) |
| Cron stops after credits run out | MiniMax Feishu Wiki (§ B-2) |
| Agent vs Open Platform credits not interchangeable | MiniMax Feishu Wiki (§ B-5) |
| Refund request | MiniMax Feishu Wiki (§ B-4) |
| How to connect Feishu | MiniMax Feishu Wiki (§ F-1) |
| Feishu unavailable / connection failed | MiniMax Feishu Wiki (§ F-3) |
| Feishu pairing fails / stuck restarting | MiniMax Feishu Wiki (§ F-7) |
| Feishu duplicate replies | MiniMax Feishu Wiki (§ F-5) |
| Add bot to Feishu group | MiniMax Feishu Wiki (§ F-8) |
| HTTP 400 / 500 / Internal server error | MiniMax Feishu Wiki (§ T-1) |
| 413 request too large | MiniMax Feishu Wiki (§ T-2) |
| Always loading / no response / timeout | MiniMax Feishu Wiki (§ T-7) |
| Conversation frozen / sudden termination | MiniMax Feishu Wiki (§ T-8) |
| User hasn't provided chat_id | MiniMax Feishu Wiki (§ S-1) — collect it first |
| Generated files not found | MiniMax Feishu Wiki (§ G-8) |

---

## Flow A: Usage Question

1. **Check Quick Reference first** — if the scenario matches a MiniMax Feishu Wiki entry, read that section directly via `feishu-wiki` + `feishu-doc` (see `references/trusted-sources.md` § 2 for how to read).
2. If not in Quick Reference, read `references/trusted-sources.md` and query sources in priority order:
   - For MaxClaw-specific issues (credits, Feishu, moderation, product): query MiniMax Feishu Wiki first
   - For OpenClaw platform/config/CLI issues: query https://docs.openclaw.ai/ via `extract_content_from_websites`
3. Keywords: feature name, config field name, channel name (e.g. "feishu", "long polling", "webhook")
4. Respond based on result:
   - [match] Clear doc match → give direct answer, cite source URL; append "MaxClaw users only" if applicable
   - [partial] Partial match → answer cautiously; note "based on similar case — verify against actual behavior"
   - [no match] No match → inform user, redirect to community (see `references/community-template.md`)

---

## Flow B: Runtime Problem

### B-1: Classify

| Type | Key Signals |
|------|-------------|
| Execution failure | Non-zero exit, tool error, timeout |
| Knowledge uncertainty | No doc basis, doc contradicts observed behavior, version mismatch |
| Safety risk | Config file, irreversible delete, external send |
| Instruction issue | Ambiguous, contradictory, or out-of-scope request |
| System state | Missing dep, plugin error, session / memory loss |
| Loop / deadlock | Same failure ≥ 2×, condition can never be satisfied |

### B-2: Query Docs

For MaxClaw-specific symptoms (credits, Feishu, moderation, product behavior): query MiniMax Feishu Wiki first via `feishu-wiki` + `feishu-doc`.
For platform/config/CLI issues: query https://docs.openclaw.ai/ via `extract_content_from_websites`.
Use exact error text, operation name, or config field as keywords.

- [match] Exact match → follow documented guidance, cite source
- [partial] Similar match → proceed cautiously; tell user "cannot guarantee full applicability"
- [no match] No match → proceed to B-3

### B-3: Self-Assess

Proceed independently only if **all** are true:
- [ ] Operation is reversible, or risk is known and controlled
- [ ] Does not touch `openclaw.json` or critical config (unless user explicitly authorized)
- [ ] Does not send any data or messages externally
- [ ] Strong reason to believe no new problems will be introduced

Any condition unmet → stop, go to B-4.

### B-4: Escalate

Stop attempting. Report to user:
1. Sources consulted and findings
2. Clear problem description
3. Approaches ruled out and why
4. Use `references/community-template.md` to redirect to official support

---

## Hard Limits

- Never modify `openclaw.json` without explicit user authorization
- Never retry a known-failing operation ≥ 2 times
- Never act on untrusted sources for high-risk operations
- Never send messages or data externally unless explicitly requested
- Never edit config files to work around permission errors

---

## References

- `references/trusted-sources.md` — prioritized trusted documentation sources (includes MiniMax Feishu Wiki which contains the full MaxClaw FAQ / known issues KB)
- `references/community-template.md` — template for redirecting users to official community
