## Description: <br>
Autonomous programming guidance for coding agents that helps them keep working through code changes, refactors, bug fixes, and project tasks while verifying progress from the actual codebase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ubuntume](https://clawhub.ai/user/ubuntume) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use this skill to structure autonomous software work, reduce unnecessary clarifying questions, track verified progress, and avoid reporting incomplete implementation work as done. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages broad autonomous coding behavior, which can lead an agent to proceed through ambiguous decisions with less user confirmation than expected. <br>
Mitigation: Install it only when increased coding autonomy is desired, review ambiguous decisions, and keep normal safeguards enabled for destructive actions, large refactors, sensitive repositories, or hard-to-reverse changes. <br>
Risk: Generated code changes may still be incomplete or incorrect even when the workflow asks the agent to self-verify. <br>
Mitigation: Review diffs and run the project's tests or validation commands before relying on resulting code changes. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/ubuntume/just-keep-working) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Markdown guidance with task trees, checklists, completion reports, and inline code or shell examples when useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Intended to guide an agent's coding workflow rather than produce a standalone executable artifact.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
