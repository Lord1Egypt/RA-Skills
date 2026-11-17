## Description:

MySearch is an OpenClaw search skill that aggregates Tavily, Firecrawl, Exa, and optional X/social search behind one proxy-first path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skernelx](https://clawhub.ai/user/skernelx)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use MySearch to install, configure, and invoke a bundled search workflow for current web, news, documentation, GitHub, URL extraction, lightweight research, and optional X/social lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured queries and provider or proxy credentials are sent to the endpoints selected by the user's configuration.

Mitigation: Install only from a trusted publisher and configure only trusted HTTPS provider or proxy base URLs.

Risk: Production tokens can be exposed if copied into the installed skill directory or committed with local files.

Mitigation: Prefer OpenClaw skill environment injection and avoid storing production secrets in .env files inside the skill directory.

Risk: An untrusted proxy endpoint can observe search queries and any credentials routed through it.

Mitigation: Point MYSEARCH_PROXY_BASE_URL only at a proxy endpoint the operator controls or explicitly trusts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/skernelx/skills/mysearch)
- [ClawHub Publisher Profile](https://clawhub.ai/user/skernelx)
- [MySearch Proxy Repository](https://github.com/skernelx/MySearch-Proxy)
- [MySearch OpenClaw Bundle](https://github.com/skernelx/MySearch-Proxy/tree/main/openclaw)
- [Artifact README](artifact/README_EN.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON search, extraction, research, and health-check output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source URLs and citations when providers return them; defaults to small result sets for initial searches.]

## Skill Version(s):

0.1.11 (source: server release metadata, SKILL.md frontmatter, runtime package)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
