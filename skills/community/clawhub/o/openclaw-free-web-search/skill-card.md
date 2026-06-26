## Description: <br>
OpenClaw skill for source-backed web search, page reading, and evidence-aware claim checking, with no API keys required by default and optional providers for stronger coverage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wd041216-bit](https://clawhub.ai/user/wd041216-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search the web, read source pages, verify concrete claims, and prepare citation-ready evidence summaries. It supports a no-key default path and optional provider configuration for broader or production-oriented coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Bright Data and Web Unlocker configuration may send search queries or page URLs to a third-party provider. <br>
Mitigation: Use the no-key default path for sensitive work, and enable Bright Data or Web Unlocker only when sharing the relevant queries and URLs with that provider is acceptable. <br>
Risk: The skill installs and runs an external Python package. <br>
Mitigation: Install only from a trusted package source and review the package before deploying it in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wd041216-bit/openclaw-free-web-search) <br>
- [Project homepage](https://github.com/wd041216-bit/zero-api-key-web-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line output, with optional JSON from verification and reporting commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns source URLs, support and conflict scores, page-aware verification status, and next-step guidance when available.] <br>

## Skill Version(s): <br>
23.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
