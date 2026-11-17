## Description:

KDP Publisher DE converts Markdown chapters into professionally formatted, KDP-ready PDFs in the OpenClaw book style with QR-code support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tikitackr](https://clawhub.ai/user/tikitackr)

### License/Terms of Use:

MIT-0

## Use Case:

Authors, publishers, and developers use this skill to turn German Markdown book chapters into print-ready Amazon KDP PDFs, either chapter by chapter or as a complete book.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF compilation can send manuscript content to a remote TypeTex service.

Mitigation: Use the skill only when remote compilation is acceptable, verify the TypeTex endpoint, and avoid sensitive manuscripts unless the endpoint is trusted.

Risk: Untrusted Typst content may include directives that expose unintended local files during compilation.

Mitigation: Review inputs before execution, avoid direct Typst files with untrusted include directives, and use trusted Markdown sources.

Risk: Dependency behavior may change across environments.

Mitigation: Install dependencies in a pinned virtual environment and review the skill before installing in workflows that handle private project files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tikitackr/skills/kdp-publisher-de)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and generated PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Markdown chapter input and optional links.json configuration for QR-code targets.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
