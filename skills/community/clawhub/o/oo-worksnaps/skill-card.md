## Description:

Use this skill to search and read Worksnaps data through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using a connected OOMOL account can retrieve Worksnaps projects, tasks, assignments, time entries, and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup can execute unreviewed remote code and introduce additional persistent agent skills.

Mitigation: Review and pin the CLI before installation, approve installation separately, and set OO_SKILLS_SYNC_DISABLED=1 before invoking a compatible CLI to disable startup skill synchronization.

Risk: Connecting OOMOL mediates access to the Worksnaps account and work records; hosted connector and external installer behavior are unverified.

Mitigation: Review the setup and access before connecting, and do not assume external installer contents or hosted connector behavior have been verified.

## Reference(s):

- [Worksnaps](https://www.worksnaps.com)
- [Worksnaps API documentation](https://api.worksnaps.com/api_docs/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Text summaries and JSON connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Worksnaps data for supported project, task, assignment, time entry, and report actions.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
