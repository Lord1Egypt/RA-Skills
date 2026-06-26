## Description: <br>
OpenClaw documentation expert that answers questions about OpenClaw setup, configuration, providers, troubleshooting, and recent changes using live document fetching, BM25 search, and change tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alfonso46674](https://clawhub.ai/user/alfonso46674) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to answer OpenClaw documentation questions, locate relevant docs, fetch focused sections, search cached documentation, compare versions, and provide configuration guidance with source citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configuration snippets can enable sensitive settings such as bash or browser tools, public service binding, or provider credentials. <br>
Mitigation: Review snippets before use and apply sandboxing, authentication, least privilege, and network controls before enabling exposed services or high-impact tools. <br>
Risk: The skill fetches and caches OpenClaw documentation, so answers may depend on network availability or the freshness of local cached content. <br>
Mitigation: Use the built-in cache status, version flags, and source citations to confirm whether results come from the intended OpenClaw release or current documentation. <br>


## Reference(s): <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw website](https://openclaw.ai) <br>
- [Openclaw Sage ClawHub listing](https://clawhub.ai/alfonso46674/openclaw-sage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown answers with source citations, inline shell commands, configuration snippets, and optional JSON from helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch and cache OpenClaw documentation locally; JSON output is available for sitemap and search workflows.] <br>

## Skill Version(s): <br>
0.3.1 (source: frontmatter, package.json, CHANGELOG, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
