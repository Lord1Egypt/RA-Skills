## Description:

Manage P-Todo tasks, users, comments, settings, searches, and exports through its localhost REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pondsi](https://clawhub.ai/user/pondsi)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to operate the P-Todo desktop todo application through its local REST API, including task management, comments, users, statistics, search, settings, and data export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated API access can delete tasks, comments, users, or app data.

Mitigation: Use only in a trusted local environment, add authentication before broader use, and require explicit confirmation for destructive operations.

Risk: The export endpoint may write exported data to arbitrary file paths.

Mitigation: Restrict exports to an approved safe directory and review requested export paths before execution.

Risk: Running the API on a shared or exposed network can allow unintended control of the P-Todo app.

Mitigation: Bind the API to loopback only and avoid running the app on shared or exposed networks as-is.

## Reference(s):

- [ClawHub P-Todo Skill Page](https://clawhub.ai/pondsi/skills/p-todo)
- [P-Todo REST API Skill](artifact/SKILL.md)
- [P-Todo README](artifact/README.md)
- [P-Todo Chinese Documentation](artifact/说明.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown API reference with curl examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets a local P-Todo REST API on configurable port 9527.]

## Skill Version(s):

1.0.0 (source: server release metadata and pom.xml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
