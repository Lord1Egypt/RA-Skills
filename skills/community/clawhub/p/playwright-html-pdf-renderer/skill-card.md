## Description:

Render deterministic PDFs from HTML using local Playwright/Chromium.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asperitas-solutions](https://clawhub.ai/user/asperitas-solutions)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create stable, repeatable PDF output from HTML content with Playwright and Chromium.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable Playwright or Chromium installation can change rendering behavior across environments.

Mitigation: Install in a minimally privileged or disposable environment and pin Playwright with a lockfile when possible.

Risk: Using a cloud browser provider can expose rendered HTML content to an external service.

Mitigation: Configure a cloud browser provider only when external rendering is intended and approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asperitas-solutions/skills/playwright-html-pdf-renderer)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [PDF files with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local headless Chromium for rendering; an optional cloud browser provider requires an intentionally configured provider API key.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
