## Description:

Open-source contribution workflow - find GitHub issues, implement fixes, submit PRs, track results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kagura-agent](https://clawhub.ai/user/kagura-agent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external contributors use this skill to run a structured open-source contribution loop: find suitable GitHub issues, implement changes through delegated coding agents, submit pull requests, and track follow-up work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated agents can modify local repositories, run commands, push branches, and create pull requests.

Mitigation: Review generated diffs, test results, branch pushes, and pull request content before accepting or reusing the work.

Risk: `gogetajob watch` can create automatic sync behavior through cron.

Mitigation: Use watch mode only when you understand the scheduled job and know how to remove it.

Risk: The workflow stores follow-up notes and lessons for future use.

Mitigation: Review persistent memory or field-note updates before they are reused in later contribution work.

## Reference(s):

- [Workloop Overview](references/workloop-overview.md)
- [ClawHub Skill Page](https://clawhub.ai/kagura-agent/skills/gogetajob)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Code, Configuration]

**Output Format:** [Markdown with inline shell commands and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to modify local repositories, run commands, push branches, create pull requests, and update persistent project notes.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
