## Description:

Use AgentMesh Job Agent for resume-driven job discovery, signed review, user-confirmed delivery and audit on Boss直聘, 猎聘, 智联招聘 and 51Job.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiyangnan](https://clawhub.ai/user/jiyangnan)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers use this agent skill to find and evaluate roles against their resume, review recommendations, and authorize application delivery on supported job platforms. It guides users through account setup, confirmation, and audit steps while preserving their control over credentials and submissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is marked suspicious because its install instructions pipe a script from a mutable online source directly into a shell; the available scan also had partial coverage.

Mitigation: Review the installer source and independently verify its origin and integrity before running it; the skill documents downloading the installer for review before execution.

## Reference(s):

- [Job Agent service](https://jobagent.agentmesh360.com/)
- [ClawHub release page](https://clawhub.ai/jiyangnan/skills/job-agent)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Step-by-step workflow guidance with user confirmation before job delivery.]

## Skill Version(s):

0.6.23 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
