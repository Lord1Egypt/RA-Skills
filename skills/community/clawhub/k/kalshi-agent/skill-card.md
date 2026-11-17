## Description:

Kalshi Agent helps agents analyze Kalshi prediction markets and execute trades through the Kalshi v2 API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jthomasdevs](https://clawhub.ai/user/jthomasdevs)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent operators use this skill to browse Kalshi markets, inspect account and portfolio state, and prepare or execute Kalshi trades through the kalshi CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read Kalshi account data and place or cancel real orders.

Mitigation: Install only when live Kalshi access is intended, require explicit human approval for every trade, and do not use --force in agent workflows.

Risk: The installer uses an unpinned global kalshi-cli installation.

Mitigation: Pin and inspect the kalshi-cli version before installation and avoid running the installer with elevated privileges.

Risk: Kalshi API credentials and the private key are stored on the local filesystem.

Mitigation: Lock down ~/.kalshi and private key files to owner-only permissions.

## Reference(s):

- [Kalshi API Reference](https://docs.kalshi.com/api-reference/)
- [Kalshi API Credentials](https://kalshi.com/api)
- [kalshi-cli](https://github.com/JThomasDevs/kalshi-cli)
- [ClawHub Skill Page](https://clawhub.ai/jthomasdevs/skills/kalshi-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Kalshi API credentials and a local RSA private key before live account access or trading.]

## Skill Version(s):

0.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
