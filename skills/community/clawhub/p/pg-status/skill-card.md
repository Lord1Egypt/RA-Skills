## Description:

Use when checking ProxyGate status, including balances, usage, listings, tunnel health, earnings, seller profiles, and job status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jwelten](https://clawhub.ai/user/jwelten)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, buyers, and sellers use this skill to ask an agent for ProxyGate account and marketplace status checks such as balances, usage, listings, settlements, tunnel health, and job status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged command reference includes deposit, withdraw, authentication, listing mutation, proxy request, tunnel, and job commands that go beyond a status-only workflow.

Mitigation: Require explicit user confirmation before proposing or running any deposit, withdraw, auth change, listing change, proxy request, tunnel, or job action.

Risk: Status checks can reveal account, usage, settlement, listing, or seller information.

Mitigation: Limit output to the user's requested status scope and avoid exposing credentials, API keys, wallet keypair paths, or unnecessary account details.

## Reference(s):

- [ProxyGate CLI Command Reference](artifact/references/commands.md)
- [ProxyGate Gateway](https://gateway.proxygate.ai)
- [ClawHub Skill Page](https://clawhub.ai/jwelten/skills/pg-status)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ProxyGate CLI commands, SDK snippets, status interpretation, and cautionary guidance for actions outside status checks.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
