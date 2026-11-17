## Description:

Use the ClawHub CLI to search, install, update, and publish agent skills from clawhub.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lice2021](https://clawhub.ai/user/lice2021)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to search for ClawHub skills, install or update them, list local skills, and publish skill folders through the npm-installed ClawHub CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forced bulk updates can replace local skill files.

Mitigation: Use pinned versions where possible, confirm the target skill directory, and avoid `--all --no-input --force` unless the workspace is backed up or under version control.

Risk: Publishing authentication stores credentials for ClawHub operations.

Mitigation: Run `clawhub login` only in trusted environments and confirm where credentials are stored before publishing.

Risk: Installing from an unexpected registry or workspace can introduce unreviewed skill content.

Mitigation: Confirm the registry and workspace before installing, then review and scan the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lice2021/skills/liu)
- [ClawHub registry](https://clawhub.com)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill provides CLI command patterns and configuration notes; it does not define a structured machine-readable output contract.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
