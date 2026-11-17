## Description:

Autonomously run complex software engineering tasks like bug fixes or feature implementation using the mini-swe-agent CLI with full codebase edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c1nderscript](https://clawhub.ai/user/c1nderscript)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to delegate complex repository tasks, such as bug fixes, feature work, and GitHub issue resolution, to the mini-swe-agent CLI for autonomous codebase exploration and editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes a secondary coding agent in unattended mode, which can make unintended code changes or run commands without intermediate prompts.

Mitigation: Use the skill in an isolated repository or container, keep secrets out of the environment, review the exact command before execution, and inspect the resulting diff and command output before accepting changes.

Risk: Untrusted issue text or task descriptions could steer the autonomous coding tool toward unsafe commands or unwanted edits.

Mitigation: Avoid passing untrusted instructions directly to the command; rewrite task statements into narrow, reviewed problem descriptions before running the tool.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/c1nderscript/skills/mini-swe-agent)
- [Publisher profile](https://clawhub.ai/user/c1nderscript)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in repository file changes and command execution through the invoked mini-swe-agent CLI.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
