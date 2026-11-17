## Description:

Helps research teams manage knowledge, track project progress, prepare meeting notes and literature reviews, record experiments, assist with code and data analysis, and run daily or weekly collaboration routines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biociao](https://clawhub.ai/user/biociao)

### License/Terms of Use:

MIT-0

## Use Case:

Research teams and their AI assistants use this skill to coordinate meetings, maintain team knowledge, track project status, prepare scientific documentation, and support code or data-analysis tasks. It is intended for collaborative repositories or communication channels where team members explicitly want AI-assisted project tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring member monitoring and scheduled checks can process team activity without sufficient consent.

Mitigation: Install only for teams that explicitly agree to AI-assisted project tracking, keep heartbeat monitoring and scheduled execution off by default, and document opt-out or disable paths.

Risk: Repository writes, commits, or pushes could change team records without adequate approval.

Mitigation: Require human review before any Git commit or push and limit the files the agent can read or modify.

## Reference(s):

- [OpenClaw Research Team Collaboration Protocol](references/protocol.md)
- [Team Git repository referenced by the protocol](https://gitea.biochao.cc/BioChaoGroup/ClawNotes)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with tables, checklists, inline code, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose repository file updates, reminders, meeting summaries, task tables, and human-review checkpoints.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
