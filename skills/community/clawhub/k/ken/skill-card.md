## Description:

Thompson-mode discipline for any coding task: think first, build bottom-up, brute force until measured, rewrite over patch. Not for non-coding requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rajnandan1](https://clawhub.ai/user/rajnandan1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to steer coding agents toward Thompson-mode coding discipline: think before editing, prefer simple primitives, try working code, and rewrite units that have accumulated repeated patches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill deliberately tries to stay active across responses and can shape coding behavior broadly.

Mitigation: Install it only for coding workflows where this posture is intended, and disable it with 'stop ken' or 'normal mode' for other work.

Risk: The skill may favor rewrites and deletion of thin layers, which can expand change scope.

Mitigation: Require scoped human review and runnable checks before applying generated code changes, especially in shared or critical code.

Risk: The skill may produce terse code-first responses when fuller reasoning is needed.

Mitigation: Ask explicitly for a full explanation, or disable the skill when detailed analysis is required.

## Reference(s):

- [Project homepage](https://github.com/rajnandan1/ken)
- [ClawHub skill page](https://clawhub.ai/rajnandan1/skills/ken)

## Skill Output:

**Output Type(s):** [code, shell commands, markdown, guidance]

**Output Format:** [Markdown with code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Encourages terse code-first responses with short implementation notes unless the user requests fuller explanation.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
