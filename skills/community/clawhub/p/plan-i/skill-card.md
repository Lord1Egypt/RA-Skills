## Description:

Starts a new planning workflow and creates a new planning file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[9talk](https://clawhub.ai/user/9talk)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to initialize a Chinese-language planning document, capture an initial structured plan from the user's request, and hand off to a follow-up planning workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plan names are used in generated Markdown filenames, and unusual characters could create confusing or unintended paths.

Mitigation: Use simple kebab-case plan names without slashes, dots, shell metacharacters, or unusual characters until strict safe-name validation is added.

## Reference(s):

- [Plan I ClawHub release page](https://clawhub.ai/9talk/skills/plan-i)
- [9talk publisher profile](https://clawhub.ai/user/9talk)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown planning file and concise user-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a dated planning document under the workspace plans directory.]

## Skill Version(s):

0.1.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
