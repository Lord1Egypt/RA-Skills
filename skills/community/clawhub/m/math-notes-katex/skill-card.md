## Description:

Math Notes KaTeX renders math-heavy notes with LaTeX and KaTeX into PNG images for cases where normal chat formatting is insufficient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rokokol](https://clawhub.ai/user/rokokol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, students, and agents use this skill to turn UTF-8 notes with inline and display LaTeX into clean PNG pages for sharing in channels that do not render math well.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local renderer launches Brave with browser sandboxing disabled while processing user-controlled notes.

Mitigation: Install only after review, avoid rendering untrusted notes, and run the skill as an isolated low-privilege user or container.

Risk: Regular use with disabled browser isolation can increase exposure if the note input is unsafe.

Mitigation: Do not run it as root and consider removing the sandbox-disabling flags before regular use.

## Reference(s):

- [Formatting guide](references/formatting.md)
- [Troubleshooting guide](references/troubleshooting.md)
- [Math Notes KaTeX on ClawHub](https://clawhub.ai/rokokol/skills/math-notes-katex)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Guidance]

**Output Format:** [PNG image files generated from UTF-8 Markdown-like notes with LaTeX math]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-page and multi-page rendering; requires local KaTeX assets and a Brave or Chromium-compatible browser.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
