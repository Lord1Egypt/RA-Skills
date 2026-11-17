## Description:

Render a URL in headless Chromium and extract structured JSON or body-only raw HTML from the post-JavaScript page, with an optional LLM-assisted flow for answering application questions from a resume.

This skill is ready for commercial/non-commercial use.

## Publisher:

[umerkha2007](https://clawhub.ai/user/umerkha2007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect web pages that require JavaScript rendering, extract structured page content, or capture sanitized body HTML for downstream analysis. It is also useful for gated job-application workflows when deterministic page classification should happen before optional question answering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs a PyPI package plus a Playwright-managed Chromium browser.

Mitigation: Install only in environments where those dependencies are acceptable, and review the package and browser installation policy before deployment.

Risk: Enabling question answering can send resume contents and extracted application-page text to Anthropic.

Mitigation: Use the default deterministic rendering and parsing flow unless the LLM feature is needed; avoid unnecessary sensitive data and review provider privacy terms before enabling it.

Risk: Rendered pages can be CAPTCHA, login, error, closed-job, or bot-challenge pages instead of the intended application content.

Mitigation: Use the deterministic detection flow for job-application URLs and only run optional question answering after a page is classified as an application.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, HTML, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or HTML output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying CLI processes one URL per invocation, may write auto-incremented JSON or HTML files, and keeps LLM-based question answering off by default.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
