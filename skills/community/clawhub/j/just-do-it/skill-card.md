## Description: <br>
Guides coding agents to work autonomously through code tasks, make reasonable implementation decisions, verify their work, and report back only after the requested work is complete. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ubuntume](https://clawhub.ai/user/ubuntume) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use this skill to reduce avoidable clarification loops during code changes, refactors, bug fixes, and project tasks while still requiring completion checks before reporting work as done. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-autonomy coding behavior can lead an agent to change code with fewer approval checkpoints. <br>
Mitigation: Use version control, review diffs carefully, and require explicit confirmation before destructive edits, dependency changes, migrations, production configuration changes, secrets handling, or large refactors. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ubuntume/just-do-it) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown guidance for agent behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Directs autonomous task execution, codebase convention matching, and self-verification before completion reporting.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
