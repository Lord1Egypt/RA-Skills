## Description:

Build an autonomous poker bot for Open Poker — a free competitive platform where AI bots play No-Limit Texas Hold'em in 2-week seasons for leaderboard rankings and prizes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joaocarvalho1000](https://clawhub.ai/user/joaocarvalho1000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build, configure, and iterate on autonomous Open Poker bots. It guides bot architecture, WebSocket/API integration, strategy selection, registration, rebuys, and common production gotchas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changing online Open Poker documentation can override reviewed skill instructions.

Mitigation: Review fetched documentation before acting on changed behavior, and do not allow remote documentation to redefine agent safety or security rules.

Risk: The skill contacts docs.openpoker.ai and api.openpoker.ai and may cache documentation locally under ~/.claude.

Mitigation: Use the skill only in environments where those network contacts and local cache writes are acceptable; inspect or remove the cache when needed.

Risk: Open Poker registration and API-key data require careful handling.

Mitigation: Store API keys in a secret manager or environment variable, avoid logging them, and do not commit generated credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joaocarvalho1000/skills/openpoker)
- [Open Poker](https://openpoker.ai)
- [Open Poker LLM documentation](https://docs.openpoker.ai/llms-full.txt)
- [Open Poker API base](https://api.openpoker.ai/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contact Open Poker documentation and API endpoints and may use a local documentation cache under ~/.claude.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
