## Description:

Pingdom (pingdom.com). Use this skill for ANY Pingdom request — searching and reading data. Whenever a task involves Pingdom, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to read Pingdom uptime checks, account credit information, and probe details through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute an unpinned remote installer without clear user approval; the remote installers and live connector implementation remain unverified.

Mitigation: Install a reviewed, pinned CLI manually and prevent automatic installer execution. Review or disable managed-skill synchronization, connect only the intended Pingdom account, and account for OOMOL mediating access.

## Reference(s):

- [Pingdom API documentation](https://docs.pingdom.com/api/)
- [Pingdom](https://www.pingdom.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Pingdom skill page on ClawHub](https://clawhub.ai/oomol/skills/oo-pingdom)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Pingdom data as JSON with concise text summaries and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented results for uptime checks, account credits, and probe information.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
