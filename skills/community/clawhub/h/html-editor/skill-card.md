## Description:

HTML Editor converts static HTML into an editable page with inline text editing, style controls for color, typography and layout, style-prompt copy actions, and clean HTML export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ytisvibecoding](https://clawhub.ai/user/ytisvibecoding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and content authors use this skill to turn reports, pages, and presentation-style HTML into editable files without manually building editing controls. It is useful when an agent needs to adapt static HTML, expose style controls, and export a clean updated page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSS metadata from local HTML may be sent to Anthropic or OpenAI when ambient API keys are present.

Mitigation: Run the tool without ANTHROPIC_API_KEY or OPENAI_API_KEY, or block network access, when processing confidential HTML.

Risk: Using --skip-checks can force output even when sanity checks fail.

Mitigation: Avoid --skip-checks for normal use; manually inspect generated HTML when checks are skipped.

Risk: Edited content and style choices can persist in browser localStorage.

Mitigation: Clear or reset localStorage after handling sensitive content or when sharing the edited HTML environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ytisvibecoding/skills/html-editor)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The primary generated file is an editable HTML document; clean export removes the editor UI while preserving page edits.]

## Skill Version(s):

1.8.4 (source: server release, target metadata, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
