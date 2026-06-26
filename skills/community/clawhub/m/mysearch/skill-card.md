## Description: <br>
Default search skill for OpenClaw that aggregates Tavily, Firecrawl, Exa, and optional X/social search behind one proxy-first path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skernelx](https://clawhub.ai/user/skernelx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use MySearch to route current web, news, documentation, GitHub, pricing, changelog, extraction, research, and optional social lookups through a single configured search skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and configured credentials may be sent to the proxy or external providers selected by the user. <br>
Mitigation: Use a proxy endpoint you control or trust, prefer dedicated low-privilege API keys, and inject secrets through OpenClaw skill env rather than copying .env files. <br>
Risk: Implicit invocation can route external lookup requests to configured search providers automatically. <br>
Mitigation: Install MySearch only when you want it to be the default external lookup route and review provider configuration before enabling it in shared environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skernelx/mysearch) <br>
- [Publisher profile](https://clawhub.ai/user/skernelx) <br>
- [MySearch OpenClaw bundle](https://github.com/skernelx/MySearch-Proxy/tree/main/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line output with URLs and source summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include external URLs, provider status, citations, extracted page text, and provider-specific errors.] <br>

## Skill Version(s): <br>
0.1.11 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
