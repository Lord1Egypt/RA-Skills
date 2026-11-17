## Description:

Manage NetPad forms, submissions, users, RBAC, and marketplace app installs through REST API and CLI guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrlynn](https://clawhub.ai/user/mrlynn)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to create and publish NetPad forms, submit and query form data, manage users, groups, roles, and install NetPad marketplace apps. It is intended for agents helping with NetPad account administration and automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad live NetPad account actions, including destructive deletes and RBAC changes.

Mitigation: Use least-privilege NetPad API keys, prefer a test project first, and verify every form, submission, organization, user, group, and role ID before execution.

Risk: Submission exports may contain sensitive data.

Mitigation: Export submissions only in approved contexts and handle exported files according to the data sensitivity of the target form.

Risk: The NetPad CLI install is described as a global package install without a pinned version.

Mitigation: Pin or otherwise verify the @netpad/cli package before installing it globally.

Risk: The helper script allows NETPAD_BASE_URL overrides.

Mitigation: Use only trusted NetPad API base URLs and avoid arbitrary or unreviewed endpoint overrides.

## Reference(s):

- [NetPad Skill Page](https://clawhub.ai/mrlynn/skills/netpad)
- [NetPad API v1 - Complete Endpoint Reference](artifact/references/api-endpoints.md)
- [NetPad CLI Reference (@netpad/cli)](artifact/references/cli-commands.md)
- [Michael Lynn Website](https://mlynn.org)
- [mrlynn GitHub Profile](https://github.com/mrlynn)
- [Michael Lynn LinkedIn Profile](https://linkedin.com/in/mlynn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose REST API calls, NetPad CLI commands, helper script usage, and JSON payloads for form and submission workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
