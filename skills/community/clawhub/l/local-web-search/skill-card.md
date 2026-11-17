## Description:

Local Web Search gives agents real-time web search, page browsing, factual claim verification, and optional Gemini-backed Google Search grounding while preferring local SearXNG and Scrapling paths by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psanger](https://clawhub.ai/user/psanger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let OpenClaw-style agents search the web, read pages, verify factual claims, and produce current-information answers with source context. The normal path favors local/private search, with Gemini-backed Google Search grounding available only when explicitly requested or local engines are insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs and make outbound web requests from the runtime environment.

Mitigation: Run it with egress controls, and avoid environments where localhost, private services, or cloud metadata endpoints are reachable unless those routes are blocked.

Risk: Gemini mode can use sensitive API credentials and sends the raw search query to Google's Gemini API.

Mitigation: Use scoped credentials, pass only the search question, and avoid sourcing broad secrets.env files into shared agent sessions.

Risk: Browsing can be delegated to a configured browser worker.

Mitigation: Configure BROWSER_WORKER_URL only for a trusted worker that is intentionally reachable from the caller's network.

Risk: The Gemini wrapper can create a virtual environment and install an unpinned google-genai dependency.

Mitigation: Review or pin the dependency before using the wrapper in managed or production-like environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/psanger/skills/local-web-search)
- [Declared project homepage](https://github.com/wd041216-bit/openclaw-free-web-search)
- [Scrapling](https://github.com/D4Vinci/Scrapling)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Plain text, Markdown-style answers, or JSON search, browsing, and verification results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include source URLs, snippets or extracted page text, confidence indicators, verification verdicts, and Gemini grounding citations when available.]

## Skill Version(s):

4.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
