## Description:

Use an OOMOL-connected account to read Hotjar surveys and responses, and submit user lookup requests that can optionally delete matching data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve survey definitions and responses, list surveys, or submit organization user lookup requests in their connected Hotjar account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified remote code and introduce broader agent changes without clear user approval.

Mitigation: Review the setup, use a vetted fixed CLI release, explicitly approve local installation changes, and review or disable automatic skill synchronization.

Risk: A user lookup can optionally delete matching Hotjar data.

Mitigation: Confirm the exact target before any deletion.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Hotjar](https://www.hotjar.com/)
- [Hotjar API Reference](https://help.hotjar.com/hc/en-us/articles/36820005914001-Hotjar-API-Reference)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured Hotjar data in JSON with concise task guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Survey responses may use cursor pagination; user lookup can optionally delete matching data.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
