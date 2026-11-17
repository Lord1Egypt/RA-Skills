## Description:

Implements a JavaScript literal syntax-based protocol for LLM tool calls. Invoke when needing to enable LLM to call local JS functions using template literal syntax.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roryyu](https://clawhub.ai/user/roryyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to describe and implement a JavaScript tagged-template protocol that lets an LLM propose calls to local JavaScript functions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LLM-generated output could trigger local JavaScript function execution without clear scoping or safety controls.

Mitigation: Use the protocol only in a controlled JavaScript environment with a small allowlist of harmless functions, strict argument validation, sandboxing or permission boundaries, and explicit human or developer approval before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roryyu/skills/js-literals-protocol)

## Skill Output:

**Output Type(s):** [Guidance, Code]

**Output Format:** [Markdown with JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; execution requires a controlled JavaScript runtime and approved local functions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
