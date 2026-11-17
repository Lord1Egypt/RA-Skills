## Description:

Compresses prompts and context by retaining high-information sentences while reducing redundant text and token use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can shorten long prompts or documents to fit context windows or reduce per-turn token use, then review the result before reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compression can omit important nuance even when key sentences appear to be retained.

Mitigation: Compare the result with the original before reuse, especially for legal, medical, financial, security, or policy text.

Risk: An undocumented integration suggestion may be unreliable.

Mitigation: Use the documented command-line entry point rather than importing from __pycache__.

## Reference(s):

- [Prompt Compressor on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/prompt-compressor)
- [LGD theory (background)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text with a compressed prompt and compression report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports sentence counts and checks retention of detected constraints, numbers, and code blocks.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata; artifact declares 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
