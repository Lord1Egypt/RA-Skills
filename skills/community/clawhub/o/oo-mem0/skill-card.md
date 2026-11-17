## Description:

Mem0 (mem0.ai). Use this skill for ANY Mem0 request — reading, creating, updating, and deleting data. Whenever a task involves Mem0, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents can use this skill to search and inspect Mem0 memories, events, and users, and to add, update, or delete memories through an OOMOL-connected account. The user needs the oo CLI installed and Mem0 connected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI installers were unavailable for inspection, so their full local effects are unverified.

Mitigation: Review the CLI and installer separately, then install the CLI only when needed.

Risk: The CLI may synchronize agent skills at startup and add persistent skills.

Mitigation: Decide whether synchronization is acceptable; set OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization.

Risk: OOMOL has access to the connected Mem0 account and submitted data.

Mitigation: Review the data and account scope being shared through the connection before using the skill.

## Reference(s):

- [Mem0](https://mem0.ai)
- [Mem0 platform quickstart](https://docs.mem0.ai/platform/quickstart)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON service responses with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read operations are distinguished from writes and deletions; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.6 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
