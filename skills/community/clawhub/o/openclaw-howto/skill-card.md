## Description: <br>
OpenClaw HowTo provides guidance on OpenClaw features, configuration, CLI commands, troubleshooting, and best practices using web search when available and local OpenClaw information when web search is unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sparkmilkway](https://clawhub.ai/user/sparkmilkway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to answer OpenClaw usage questions, configure OpenClaw features, inspect CLI behavior, and troubleshoot agents, cron jobs, skills, gateway services, and related settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide CLI mutations and configuration changes. <br>
Mitigation: Review every suggested remove, uninstall, write/edit, bulk, or shell command before allowing an agent to run it. <br>
Risk: The skill stores environment-specific configuration and search or troubleshooting notes in memory. <br>
Mitigation: Do not provide tokens, internal endpoints, secret-bearing examples, or sensitive error logs. <br>
Risk: The skill may provide command examples that are unsafe to copy and run without context. <br>
Mitigation: Treat commands as proposals and adapt them to the local environment after manual review. <br>


## Reference(s): <br>
- [OpenClaw HowTo Skill](https://clawhub.ai/sparkmilkway/openclaw-howto) <br>
- [OpenClaw Best Practices Guide](artifact/references/best-practices.md) <br>
- [OpenClaw Command Cheatsheet](artifact/references/commands-cheatsheet.md) <br>
- [OpenClaw Search Strategy Guide](artifact/references/search-strategies.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend OpenClaw CLI commands, local file reads, configuration updates, or web search depending on available tools.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
