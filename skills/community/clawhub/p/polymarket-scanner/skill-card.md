## Description:

Automated Polymarket prediction market scanner and trader via the Simmer API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wyzmf](https://clawhub.ai/user/wyzmf)

### License/Terms of Use:


## Use Case:

External developers and operators use this skill to scan Polymarket opportunities, check balances and positions, and run configurable virtual or real-money trades through a Simmer account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically place prediction-market trades, and evidence.security says some documented safety controls are not enforced in code.

Mitigation: Review before installing, use only an account and API key acceptable for trading, start with dry-run or read-only evaluation, and avoid scheduling until execution limits and confirmation behavior are clear.

Risk: The scanner requires SIMMER_API_KEY credentials to access a Simmer account.

Mitigation: Use the least-privileged or lowest-risk account available, avoid sharing the key, and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wyzmf/skills/polymarket-scanner)
- [Simmer Markets](https://simmer.markets)
- [Simmer API endpoint](https://api.simmer.markets/api/sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [CLI text output with optional JSONL trade log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and may call the Simmer API when executed.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
