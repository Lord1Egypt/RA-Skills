## Description:

Use Runscope for search and read requests instead of calling its API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Runscope accounts, buckets, tests, environments, and recent test results through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup executes remote code, and startup skill synchronization can make persistent agent changes. The installer and hosted connector implementation have not been verified.

Mitigation: Review and approve the CLI installation separately using a verified release. Set OO_SKILLS_SYNC_DISABLED to disable startup synchronization, and understand that OOMOL handles the Runscope connection and credentials.

## Reference(s):

- [Runscope API documentation](https://api.runscope.com/docs)
- [Runscope API Monitoring](https://www.blazemeter.com/api-monitoring)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Runscope skill release](https://clawhub.ai/oomol/skills/oo-runscope)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON responses and shell command instructions, with usage guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only account, bucket, environment, test, and test-result operations.]

## Skill Version(s):

1.0.4 (source: server-resolved release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
