## Description:

CLI web search and page fetcher for LLM agents that searches DuckDuckGo, Brave, Bing, or Google, fetches pages as markdown, and extracts links without a browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neothelobster](https://clawhub.ai/user/neothelobster)

### License/Terms of Use:


## Use Case:

Developers and agents use Ghostfetch to search the web, fetch page content as markdown or JSON, and extract links while gathering information from the web.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs an externally built binary that is not fully contained in the submitted package.

Mitigation: Install only if comfortable building and running code from the referenced Ghostfetch repository; prefer the pinned setup path and audit upstream source when stronger assurance is required.

Risk: Persisted cookies may expose sensitive browsing state.

Mitigation: Avoid using persisted cookies for sensitive browsing and use the no-cookie mode where appropriate.

Risk: CAPTCHA service API keys may be exposed on shared systems.

Mitigation: Avoid passing CAPTCHA API keys on shared systems.

Risk: Read-only and no-secret-leak claims are not independently verified by the submitted package.

Mitigation: Treat those claims as unverified unless the upstream source is audited.

## Reference(s):

- [Ghostfetch ClawHub skill page](https://clawhub.ai/neothelobster/skills/ghostfetch)
- [Ghostfetch source repository referenced by artifact](https://github.com/neothelobster/ghostfetch)
- [Go downloads](https://go.dev/dl/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; Ghostfetch can return text, markdown, raw HTML, or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports web search, page fetching, link extraction, parallel fetches, browser fingerprint selection, optional cookie persistence, and optional CAPTCHA service credentials.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
