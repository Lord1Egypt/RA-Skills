## Description:

Delegates to Meta's Muse Code CLI (muse)

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill when delegation-core selects Muse for repository-scale coding work or unattended tasks. It provides setup, authentication, and invocation guidance for Muse Code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags the remote installer as unverified and reports a mismatch between the documented delegation purpose and the installer command.

Mitigation: Review the installer source and official Muse Code documentation before running it, and proceed only if you trust the installer and its requested account permissions.

Risk: Repository content may be sent to Meta during delegation.

Mitigation: Review which repository files will be included in the prompt before invoking Muse.

## Reference(s):

- [Project homepage (Clawdis metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/conjure)
- [Muse Code documentation](https://dev.meta.ai/docs/muse-code)
- [Muse Code configuration](https://dev.meta.ai/docs/muse-code/configuration)
- [Muse models](https://dev.meta.ai/docs/models)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegated results are saved to delegations/muse/YYYYMMDD_HHMMSS.md.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
