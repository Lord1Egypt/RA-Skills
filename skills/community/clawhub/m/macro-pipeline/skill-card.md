## Description:

Create and manage macro-task pipelines for QA, roadmaps, and feature rollouts using a PIPELINE.md and HEARTBEAT.md workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[santacruzg282-cyber](https://clawhub.ai/user/santacruzg282-cyber)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to define autonomous, multi-step project pipelines with repo-tracked state, heartbeat scheduling, verification commands, and subagent handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring background agents can make unattended edits, run commands, and commit changes with broad repository impact.

Mitigation: Use the skill only in repositories where unattended agent edits and commits are acceptable, and require approval or pinned execution before cron jobs run mutable pipeline steps.

Risk: External Discord notifications can disclose project details from confidential repositories.

Mitigation: Remove Discord notification steps or tightly control the destination before using the skill with confidential projects.

Risk: Broad staging with git add . can include unrelated or sensitive files in commits.

Mitigation: Replace git add . with explicit file staging for the pipeline files and expected artifacts.

## Reference(s):

- [Macro Pipeline ClawHub release](https://clawhub.ai/santacruzg282-cyber/skills/macro-pipeline)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PIPELINE.md and HEARTBEAT.md templates, cron commands, verification commands, and git commit/tag guidance.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
