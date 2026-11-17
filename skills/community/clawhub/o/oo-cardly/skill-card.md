## Description:

Use the oo CLI to access Cardly account balances, credit history, fonts, media options, and writing styles through OOMOL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to query Cardly account balances, credit history, fonts, media options, and writing styles through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs a remote installer whose behavior has not been verified and whose approval path is unclear.

Mitigation: Arrange a separately approved, verified oo installation and check its bundled-skill installation and update behavior before allowing the agent to run it.

Risk: Cardly requests pass through the connected OOMOL account, and write actions can change account state.

Mitigation: Connect only the intended Cardly account and review the exact write payload and effect before running it.

## Reference(s):

- [Cardly homepage](https://www.card.ly)
- [Cardly API documentation](https://api.card.ly/v2/docs)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [JSON responses summarized in text; oo CLI shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-dependent account and catalog data; the echo action is marked as a write.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
