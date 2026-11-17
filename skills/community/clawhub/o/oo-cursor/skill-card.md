## Description:

Connects an agent to Cursor cloud sessions through OOMOL for session management, run execution, usage reporting, and audit review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Cursor team users use this skill to manage Cursor cloud-agent sessions, submit and inspect runs, review team usage and audit activity, and view available models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI installation uses remote installers whose full effects are unverified and may change agent skill files.

Mitigation: Review and approve CLI installation separately, inspect the skill files it installs or updates, and disable automatic skill synchronization if unwanted.

Risk: Some Cursor actions create runs or agents, change session state, or permanently delete sessions.

Mitigation: Keep confirmation requirements for cloud-agent creation, other writes, and deletion; check the target and action before execution.

## Reference(s):

- [Cursor](https://cursor.com)
- [Cursor API documentation](https://cursor.com/docs/api)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, API calls, Guidance]

**Output Format:** [Structured Cursor action results and JSON payloads, with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Cursor account and the selected action.]

## Skill Version(s):

1.0.6 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
