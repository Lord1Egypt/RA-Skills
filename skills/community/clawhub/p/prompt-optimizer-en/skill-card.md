## Description:

Iterative prompt optimizer for complex tasks that implements ACON's two-stage iterative optimization and APE automatic prompt engineering, activates only on explicit request, collects feedback after optimization, and supports multi-round iteration until the user is satisfied.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ucsdzehualiu](https://clawhub.ai/user/ucsdzehualiu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, prompt authors, and agent users use this skill to turn complex prompts into clearer, more complete, and more concise instructions while preserving intent, constraints, output format, examples, tool rules, and success criteria. It is intended for explicit prompt-optimization requests and supports follow-up refinement based on user feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optimized prompts could change sensitive or high-impact instructions if accepted without review.

Mitigation: Review optimized prompts before use and verify that critical constraints, formats, tool rules, and safety boundaries are preserved.

Risk: The skill is designed to rewrite prompts only when explicitly requested; using it outside that context could produce unwanted prompt changes.

Mitigation: Activate it only for explicit requests such as optimize prompt, improve prompt, or refine instruction.

## Reference(s):

- [ACON paper (arXiv:2510.00615)](https://arxiv.org/abs/2510.00615)
- [APE paper (arXiv:2211.01910)](https://arxiv.org/abs/2211.01910)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown response with the optimized prompt in a fenced code block and a follow-up feedback question]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single response per optimization round; may iterate when the user provides feedback.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
