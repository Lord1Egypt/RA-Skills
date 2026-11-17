## Description:

Intelligently compresses and optimizes agent context to reduce token usage using deduplication, pruning, summarization, and adaptive learning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlaspa](https://clawhub.ai/user/atlaspa)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to compress long or repetitive agent context, track token savings, and inspect optimizer statistics through CLI commands or a local dashboard. It can also manage free and Pro compression tiers through x402 payment flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic context compression may remove or change information before a request reaches the model.

Mitigation: Scope compression to appropriate conversations, review behavior before production use, and disable or adjust compression for sensitive or high-precision tasks.

Risk: The skill stores usage, pattern, wallet, and payment metadata locally.

Mitigation: Avoid sensitive conversations unless compression and learning scope are acceptable; restrict access to the local data directory and periodically clear retained data.

Risk: Autonomous payment flows can spend from a funded wallet and the artifact describes MVP-level transaction verification.

Mitigation: Require manual confirmation for every payment, use limited-balance wallets, and verify transaction handling before enabling Pro purchase flows.

Risk: Dashboard APIs may expose compression data or payment operations if reachable beyond localhost.

Mitigation: Keep the dashboard bound to localhost behind authentication and do not expose port 9092 on untrusted networks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/atlaspa/skills/openclaw-context-optimizer)
- [README](artifact/README.md)
- [Agent Payments via x402](artifact/AGENT-PAYMENTS.md)
- [Compressor API](artifact/src/COMPRESSOR_API.md)
- [Quick Start](artifact/src/QUICK_START.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown, with code blocks preserved when present]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify request context before model calls and records local usage, pattern, wallet, and payment metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
