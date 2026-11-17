## Description:

Use AgentMesh Job Agent for resume-driven job discovery, signed review, user-confirmed delivery and audit on Boss直聘, 猎聘, 智联招聘 and 51Job.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiyangnan](https://clawhub.ai/user/jiyangnan)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers use the skill to discover and review opportunities on supported Chinese recruiting platforms, then approve application delivery and inspect an audit summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic installer recovery may lack the verification safeguards used for normal updates.

Mitigation: Verify a fixed installer and client revision before installation; require manual review if an update fails integrity checks.

Risk: Resume information is sent to AgentMesh360 and recruiting sessions remain stored locally; an application could expose sensitive information to an unintended recipient.

Mitigation: Carefully review each application's recipient, resume and message before approving delivery.

## Reference(s):

- [AgentMesh Job Agent](https://jobagent.agentmesh360.com/)
- [ClawHub skill listing](https://clawhub.ai/jiyangnan/skills/job-agent)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Guidance]

**Output Format:** [Command-line workflows and concise review and audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Job Agent CLI; application delivery requires user confirmation.]

## Skill Version(s):

0.6.22 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
