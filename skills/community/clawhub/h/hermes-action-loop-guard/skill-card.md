## Description:

Adds tested Hermes guard installers for the 1.2-to-1.3 redirect upgrade path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ambitioncn](https://clawhub.ai/user/ambitioncn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators maintaining Hermes installations use this skill to inspect loop states, install action-promise or tool-progress guards with compatibility checks, and verify or roll back the changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently patches Hermes agent code, configuration, and user service behavior.

Mitigation: Install only when those persistent changes are intended; test in a controlled environment, review exact diffs, run compatibility checks and dry-runs, then verify after installation.

Risk: Rollback handling can expose operators to unsafe backup manifests.

Mitigation: Run rollback only with the exact backup directory created and controlled by the operator for the relevant installation.

Risk: Guard changes can trigger additional tool execution through bounded strategy redirects.

Mitigation: Confirm that redirect behavior and stop thresholds match the operational policy before deploying to a live Hermes environment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ambitioncn/skills/hermes-action-loop-guard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and file-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for applying bundled installers, reviewing dry-run output, verifying installation, and rolling back from manifest backups.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
