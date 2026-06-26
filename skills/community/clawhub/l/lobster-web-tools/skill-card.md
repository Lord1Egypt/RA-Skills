## Description: <br>
Guides agents in choosing between web_search, web_fetch, opencli, and browser workflows, including fallback handling, search API setup, login confirmation, and site reference lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freeman88-tch](https://clawhub.ai/user/freeman88-tch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route web research tasks across search, fetch, structured CLI access, and browser automation while handling failures and credential setup explicitly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to install opencli, store API keys, and restart or kill browser and gateway processes. <br>
Mitigation: Install only after reviewing the setup script and opencli source; use low-value API keys; do not let the agent read keys back into chat; confirm Chrome, gateway, Docker, or pkill restart commands before execution. <br>
Risk: Browser and opencli workflows may access logged-in sessions or perform write actions on supported sites. <br>
Mitigation: Require user authorization before login, posting, deletion, payment, follow, block, like, or other account-changing actions. <br>


## Reference(s): <br>
- [OpenCLI Guide](references/opencli-guide.md) <br>
- [Web Search API Configuration](references/web-search-config.md) <br>
- [Well-Known Sites Index](references/well-known-sites.json) <br>
- [ClawHub Release Page](https://clawhub.ai/freeman88-tch/lobster-web-tools) <br>
- [OpenCLI Releases](https://github.com/jackwener/opencli/releases) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration steps, and JSON reference lookups] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API key handling steps, opencli setup commands, and browser or gateway restart guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: target metadata, release evidence, and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
