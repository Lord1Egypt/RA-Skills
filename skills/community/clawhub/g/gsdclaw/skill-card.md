## Description: <br>
Spec-first execution workflow for OpenClaw that turns large, vague, or messy project requests into phased, verifiable implementation plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cirokk](https://clawhub.ai/user/cirokk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical project teams use this skill to turn broad or messy app, feature, refactor, redesign, and rescue requests into phased plans with acceptance criteria, incremental execution, and verification checkpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad coding requests may lead an agent to inspect or modify many project files. <br>
Mitigation: Review the plan before large edits, keep changes phased, and verify diffs, builds, or tests after meaningful steps. <br>
Risk: Repositories may contain secrets, private URLs, or credentials while the workflow is gathering project context. <br>
Mitigation: Keep sensitive values out of reusable or public skill content and avoid copying credentials into generated plans or reports. <br>


## Reference(s): <br>
- [Execution Template](references/execution-template.md) <br>
- [Acceptance Checklist](references/acceptance-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Markdown plans, acceptance criteria, implementation notes, verification steps, and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; no required binaries, environment variables, credentials, external APIs, or executable code.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
