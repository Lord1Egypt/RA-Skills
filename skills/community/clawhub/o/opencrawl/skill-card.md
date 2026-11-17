## Description:

ConvoYield analyzes bot conversations with local heuristic engines to estimate conversational value, detect sentiment and micro-conversion signals, score engagement momentum, and recommend response strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcools1977](https://clawhub.ai/user/jcools1977)

### License/Terms of Use:

MIT

## Use Case:

Developers and bot builders use ConvoYield to add local conversation-value analysis and response-strategy guidance to chatbots across webchat, Slack, Discord, Telegram, WhatsApp, and OpenClaw-style integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server evidence reports a suspicious security verdict because the package includes under-disclosed cloud billing, telemetry, and cryptocurrency-like features with serious authorization and cryptography flaws.

Mitigation: Use the offline analysis engine only after review, and do not enable cloud server, telemetry, billing, marketplace, wallet, mining, or token features in production until authorization, HTTPS enforcement, credential storage, XSS handling, and cryptographic transaction validation are fixed.

Risk: Conversation analysis can identify contact, budget, referral, and competitive-intelligence signals from real users.

Mitigation: Obtain clear user consent, define data-retention rules, and review downstream use of extracted signals before processing production conversations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jcools1977/skills/opencrawl)
- [README](README.md)

## Skill Output:

**Output Type(s):** [guidance, text, code, configuration]

**Output Format:** [Python result objects, dictionaries, CLI text, and JSON-compatible analytics events]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local analysis uses heuristic pattern matching; optional cloud, telemetry, billing, marketplace, wallet, mining, and token features should be separately reviewed before production use.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, pyproject.toml, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
