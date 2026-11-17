## Description:

Use this skill to read and manage Zylvie data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Operators managing a Zylvie brand use this skill to inspect subscriptions, coupons, products, and license keys, and to make approved changes to business data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute remote code that was unavailable for inspection.

Mitigation: Review the CLI installation separately and use a verified, pinned release.

Risk: Automatic agent-skill synchronization may introduce changes beyond Zylvie.

Mitigation: Review the synchronization behavior and disable it if it is not wanted.

Risk: Changes to business data can affect coupons, products, and license records.

Mitigation: Connect only the intended Zylvie account and retain approval prompts for business-data changes.

## Reference(s):

- [Zylvie](https://zylvie.com/)
- [Zylvie API documentation](https://developers.zylvie.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and responses, plus concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive actions are labeled and require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
