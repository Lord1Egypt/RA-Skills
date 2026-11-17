## Description:

Stop before you break - four mandatory checks before every operation: search, rollback, test, scope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[p9sgr2rnrj-ux](https://clawhub.ai/user/p9sgr2rnrj-ux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent users use this skill to run a four-question preflight check before commands, deployments, configuration changes, or unfamiliar operations. It helps confirm prior research, rollback planning, validation, and impact scope before proceeding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can make persistent shell startup changes by appending the preflight install directory to the user's PATH.

Mitigation: Review install.sh before running it and consider adding PATH entries manually.

Risk: Custom install paths may be unsafe if they contain shell metacharacters.

Mitigation: Use simple trusted install paths and review the command before execution.

Risk: publish.sh is release tooling that can publish to ClawHub with a configured owner account.

Mitigation: Do not run publish.sh unless you intend to publish this package and have verified the target account and owner settings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/p9sgr2rnrj-ux/skills/preflight-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell command prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI path is interactive and blocks when any preflight check fails.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
