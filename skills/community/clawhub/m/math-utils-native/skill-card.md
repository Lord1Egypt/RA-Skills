## Description:

Performs precise math calculations by executing native OS CLI tools such as bc, python3, or PowerShell without relying on AI prediction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnyhou327](https://clawhub.ai/user/johnnyhou327)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to evaluate arithmetic expressions with local command-line calculators instead of model-generated answers. It is intended for deterministic numeric results from a single expression string.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided expressions are inserted into local shell, Python, or PowerShell commands, which can allow arbitrary host command execution.

Mitigation: Install and run only when all expressions are fully trusted; rewrite the skill to use a safe in-process math parser or strict arithmetic grammar before broader use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/johnnyhou327/skills/math-utils-native)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text numeric result or error message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts one math expression string; execution depends on local calculator tooling available on the host.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
