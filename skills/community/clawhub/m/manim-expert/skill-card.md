## Description:

Turns simple Manim animation requests into detailed LaTeX-rich prompts, runnable Manim Community Edition code, review notes, and rendering guidance for math education, science demonstrations, and technical documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shirleyshenda](https://clawhub.ai/user/shirleyshenda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and technical content creators use this skill to turn a short animation idea into a detailed Manim plan, Python code, syntax checks, and local rendering commands. It is intended for creating mathematical and scientific explainer animations with Manim Community Edition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to run newly generated Python and Manim code automatically, which may execute unsafe or unintended local behavior.

Mitigation: Use a dedicated workspace or sandbox without secrets, inspect the generated Python file, and approve the exact Manim command before rendering; consider disabling automatic execution or narrowing triggers.

## Reference(s):

- [Manim Community Edition Quick Reference](references/manim-quick-reference.md)
- [Mathematical Object Color Schemes](assets/color-schemes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance, files]

**Output Format:** [Markdown with Python code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create Manim Python files and low-quality MP4 render artifacts when command execution is enabled.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
