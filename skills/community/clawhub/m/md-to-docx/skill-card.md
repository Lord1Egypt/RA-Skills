## Description:

Converts Markdown files into formatted Word (.docx) documents with optional Word template style extraction and Mermaid diagram rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krabww](https://clawhub.ai/user/krabww)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and agents use this skill to turn Markdown drafts, reports, and book chapters into styled .docx files, optionally matching a Word template and embedding Mermaid diagrams as PNGs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mermaid rendering and dependency setup can rely on global or system-level tools such as npm packages, Chrome or Chromium, LibreOffice, and platform conversion utilities.

Mitigation: Use an isolated environment, pin dependencies, and review global npm, sudo, browser, LibreOffice, or textutil commands before allowing an agent to run them.

Risk: Processing untrusted Markdown with Mermaid enabled may exercise local browser-based rendering paths.

Mitigation: Avoid processing untrusted Markdown with Mermaid enabled, or review Mermaid diagram blocks before conversion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krabww/skills/md-to-docx)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; the bundled converter creates .docx files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May render Mermaid diagrams to PNG and embed them in generated Word documents.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
