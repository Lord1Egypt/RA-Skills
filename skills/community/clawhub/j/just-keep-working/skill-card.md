## Description:

Autonomous programming workflow for OpenClaw that guides an agent through codebase reading, additive implementation, confirmation gates, and read-back verification for coding tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ubuntume](https://clawhub.ai/user/ubuntume)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to have an agent carry out code changes, feature work, refactors, fixes, and project tasks with fewer unnecessary clarifying questions while preserving confirmation gates for destructive changes and unknowable decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages autonomous coding and may create files, add routes, or extend logic without asking when the work is considered additive.

Mitigation: Review the autonomy expectations before installation and preserve the confirmation gates for destructive changes, credentials, business decisions, and major architectural choices.

Risk: An agent could produce incorrect code changes or overstate completion if it does not verify work against actual files.

Mitigation: Use the skill's read-back and DONE-VERIFIED workflow before depending on completed steps or reporting completion.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task trees, progress updates, verification summaries, and focused user prompts for destructive or unknowable decisions.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
