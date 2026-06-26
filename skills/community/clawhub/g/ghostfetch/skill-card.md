## Description: <br>
Ghostfetch is a CLI web search and page-fetching skill for LLM agents that can search common engines, fetch pages as markdown or JSON, and extract links without a browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neothelobster](https://clawhub.ai/user/neothelobster) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Ghostfetch to gather web information during research workflows by running searches, converting pages to readable markdown or structured JSON, and extracting relevant links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script builds an external binary from a pinned source commit. <br>
Mitigation: Install only when you trust the pinned Ghostfetch source and are comfortable building a local binary. <br>
Risk: Fetched pages, cookies, or captcha provider keys can expose private browsing context or secrets. <br>
Mitigation: Use --no-cookies for stateless browsing, avoid private or internal URLs and pages containing secrets, and provide captcha API keys only when intentionally using those third-party services. <br>
Risk: Outbound web requests go directly from the user's machine to selected websites and search engines. <br>
Mitigation: Use Ghostfetch only in environments where outbound web access is allowed, and review fetched content before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neothelobster/ghostfetch) <br>
- [Publisher profile](https://clawhub.ai/user/neothelobster) <br>
- [Go downloads](https://go.dev/dl/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text, Markdown, JSON, or raw HTML depending on command flags] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search result limits, request timeout, browser fingerprint, parallel fetch count, cookie persistence, and captcha-provider options are configurable through CLI flags.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
