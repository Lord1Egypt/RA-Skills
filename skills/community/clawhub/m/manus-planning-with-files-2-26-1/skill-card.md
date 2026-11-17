## Description:

Implements Manus-style file-based planning to organize and track progress on complex tasks by creating task_plan.md, findings.md, and progress.md, with support for session recovery after context clears.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kakaxiazai](https://clawhub.ai/user/kakaxiazai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to keep multi-step work organized across long sessions by maintaining persistent planning, findings, and progress files in the project workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project plan text may be repeatedly injected into the agent context.

Mitigation: Use the skill only in trusted workspaces and review existing task_plan.md content before enabling it.

Risk: Session catch-up may expose prior conversation content, including sensitive prompts, credentials, or private file paths.

Mitigation: Disable or avoid session catch-up when previous sessions may contain sensitive information, and review any catch-up output before using it.

Risk: Planning files can contain untrusted web or repository content that later influences agent behavior.

Mitigation: Keep external findings in findings.md, treat fetched content as untrusted, and avoid copying instruction-like external text into task_plan.md.

## Reference(s):

- [Manus Context Engineering Principles](references/reference.md)
- [Planning with Files Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/kakaxiazai/skills/manus-planning-with-files-2-26-1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown planning files with inline shell commands and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates task_plan.md, findings.md, and progress.md in the active project workspace.]

## Skill Version(s):

2.26.1 (source: skill metadata); ClawHub release 1.0.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
