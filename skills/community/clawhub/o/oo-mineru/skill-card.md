## Description:

Operate MinerU through an OOMOL-connected account to create extraction tasks and batches and retrieve their results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing users can use the skill to submit MinerU extraction jobs through their connected OOMOL account and retrieve job status and result URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may make undisclosed changes to other agents’ skills.

Mitigation: Review setup before installation, provision a verified CLI release, and consider setting OO_SKILLS_SYNC_DISABLED=1 before invocation.

Risk: Document URLs are processed through OOMOL and MinerU.

Mitigation: Share only document URLs approved for processing through those services.

## Reference(s):

- [MinerU](https://mineru.net)
- [MinerU API documentation](https://mineru.net/apiManage/docs)
- [oo CLI commands reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON request and response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes extraction task or batch status and result URLs when available.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
