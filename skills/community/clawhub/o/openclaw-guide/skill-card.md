## Description: <br>
Authoritative OpenClaw guidance and documentation lookup. Provides accurate information about OpenClaw capabilities, configuration, and usage based on official sources (docs.openclaw.ai and github.com/openclaw/openclaw). Use when users ask about OpenClaw features, setup, configuration, troubleshooting, or any OpenClaw-related topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Linux2010](https://clawhub.ai/user/Linux2010) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and OpenClaw users use this skill to answer questions about OpenClaw setup, configuration, architecture, troubleshooting, and workflows from official documentation and source references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use web searches or fetches to answer OpenClaw questions, so responses can depend on the availability and current content of official sources. <br>
Mitigation: Review cited documentation or source links before acting on configuration, setup, or troubleshooting guidance. <br>
Risk: The optional GitHub helper script may use a local GitHub CLI if an agent or user chooses to run it. <br>
Mitigation: Run helper scripts only in an environment where GitHub CLI access and repository queries are expected and permitted. <br>


## Reference(s): <br>
- [OpenClaw official documentation](https://docs.openclaw.ai) <br>
- [OpenClaw source repository](https://github.com/openclaw/openclaw) <br>
- [OpenClaw community](https://discord.com/invite/clawd) <br>
- [Common OpenClaw queries](references/common_queries.md) <br>
- [OpenClaw documentation structure](references/docs_structure.md) <br>
- [ClawHub skill page](https://clawhub.ai/Linux2010/openclaw-guide) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with links and inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cite official OpenClaw documentation or source links when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
