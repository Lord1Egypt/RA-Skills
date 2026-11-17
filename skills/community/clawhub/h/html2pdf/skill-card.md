## Description:

Converts an HTML file, report, or webpage snapshot to PDF using headless Chrome through Puppeteer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[owenrao](https://clawhub.ai/user/owenrao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to export local HTML reports or documents as single-page poster-style PDFs or paginated A4/Letter PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs supplied HTML in a headless browser with sandboxing disabled.

Mitigation: Run conversions for untrusted or sensitive documents in an isolated, low-privilege environment and avoid the default no-sandbox mode when the environment supports browser sandboxing.

Risk: HTML conversion can contact external services while loading fonts, images, scripts, or other page resources.

Mitigation: Block network access for sensitive inputs and package all required assets locally before conversion.

Risk: Puppeteer and transitive npm dependencies affect the browser execution surface.

Mitigation: Install from the bundled lockfile with npm ci or otherwise pin, review, and update Puppeteer and transitive dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/owenrao/skills/html2pdf)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with shell commands; generated artifact is a PDF file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-page and paginated PDF modes with optional page format, viewport width, wait time, and header/footer settings.]

## Skill Version(s):

1.0.0 (source: server release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
