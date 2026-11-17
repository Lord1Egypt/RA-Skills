## Description:

Create low-fidelity, text-based wireframes using the Markdown-UI Domain Specific Language (DSL).

This skill is ready for commercial/non-commercial use.

## Publisher:

[megabytemark](https://clawhub.ai/user/megabytemark)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, designers, and frontend engineers use this skill to draft Markdown-UI DSL wireframes, translate UI specs into frontend code, and keep paired specs and components synchronized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spec-to-code or code-to-spec synchronization can overwrite frontend components or wireframe files, especially when confirmation is bypassed.

Mitigation: Review planned synchronization changes, avoid force sync unless intentional, and keep files under version control for review and rollback.

Risk: Generated UI specs or translations may misrepresent layout intent, design tokens, or framework-specific behavior.

Mitigation: Review generated DSL and translated code against the active design system before applying it to production UI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/megabytemark/skills/markdown-ui-dsl)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown-UI DSL, Markdown guidance, and frontend code or file updates when translating or synchronizing UI specs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Synchronization may modify referenced UI spec or component files after confirmation, unless the user explicitly requests autonomous or force sync behavior.]

## Skill Version(s):

1.0.3 (source: server release, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
