## Description:

make-design-md analyzes a website URL, HTML file, or screenshot to extract design tokens and produce a Google design.md-compatible DESIGN.md document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouchang1988](https://clawhub.ai/user/zhouchang1988)

### License/Terms of Use:

MIT

## Use Case:

Developers and designers use this skill to turn a website, local HTML file, or screenshot into a structured DESIGN.md design specification, preview files, and validation or export commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running an unpinned @google/design.md CLI through npx can fetch an unexpected package version.

Mitigation: Pin @google/design.md to an exact reviewed version or run it from a lockfile-managed dependency, and avoid running npx with production credentials available.

Risk: Fetched websites are untrusted inputs and may influence generated design guidance.

Mitigation: Review generated DESIGN.md and previews before use, and keep sensitive credentials out of the agent environment while fetching pages.

Risk: The skill mandates a third-party font mirror for generated previews.

Mitigation: Replace the font mirror with local fonts or a user-approved CDN before using generated previews in controlled environments.

## Reference(s):

- [Google design.md specification](https://github.com/google-labs-code/design.md)
- [DESIGN.md template](references/design-template.md)

## Skill Output:

**Output Type(s):** [markdown, text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown DESIGN.md with YAML front matter, optional HTML preview files, and inline validation or export shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include design-token references, preview HTML, and guidance for validating or exporting with the Google design.md CLI.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
