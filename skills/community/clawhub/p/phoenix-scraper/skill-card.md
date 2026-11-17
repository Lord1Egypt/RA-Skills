## Description:

Phoenix Scraper provides a resilient three-tier web scraping helper that fails over from Brave Search API to Bright Data Web Unlocker and then Playwright for JS-rendered or bot-protected public web pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevojarvisai-star](https://clawhub.ai/user/stevojarvisai-star)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to retrieve web content from public, authorized targets that may require search-index fallback, proxy unlocking, JavaScript rendering, or X API access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full target URLs can be sent to third-party services such as Brave Search and Bright Data.

Mitigation: Use only public, authorized scraping targets; avoid internal, localhost, private-network, credential-bearing, signed, password reset, and regulated-data URLs unless allowlists, URL redaction or rejection, and provider opt-ins are added.

Risk: The browser fallback can launch Chromium against arbitrary URLs.

Mitigation: Run browser rendering in a sandboxed container or equivalent isolated environment and restrict allowed target domains before enabling the Playwright tier.

Risk: Scraping the wrong target can create policy, authorization, or data-handling risk.

Mitigation: Confirm that each target is public and authorized before use, and use the documented X API path for X.com monitoring instead of direct scraping.

## Reference(s):

- [X API v2 Reference](references/x-api.md)
- [ClawHub Skill Page](https://clawhub.ai/stevojarvisai-star/skills/phoenix-scraper)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; runtime helper returns dictionaries containing HTML, text, method, URL, and error fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires provider credentials for Brave Search, Bright Data, and optionally X API; may use Playwright for browser rendering.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
