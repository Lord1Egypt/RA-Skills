## Description: <br>
opencli helps agents browse, search, summarize, and optionally act on supported social and content sites through the user's existing Chrome login session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronwang1980](https://clawhub.ai/user/aaronwang1980) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to fetch trends, search supported platforms, inspect social feeds, check market information, and prepare content actions through opencli or a browser fallback. It is most appropriate when the user already has Chrome logged in to the target services and wants agent-assisted browsing or account workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Chrome login sessions to read private account content. <br>
Mitigation: Install only for accounts and browser profiles the user is comfortable exposing to the agent, and keep sensitive services logged out. <br>
Risk: The skill can perform account actions such as posting, replying, liking, deleting, checking in, or using a Playwright fallback. <br>
Mitigation: Require explicit user confirmation before any write action or browser fallback that could affect an account. <br>
Risk: The skill can persist generated site automations under ~/.opencli/clis. <br>
Mitigation: Periodically inspect generated automation files and remove entries that are no longer trusted or needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaronwang1980/opencli-skill) <br>
- [opencli upstream project](https://github.com/jackwener/opencli) <br>
- [opencli command reference](references/commands.md) <br>
- [Playwright MCP Bridge](https://chromewebstore.google.com/detail/playwright-mcp-bridge/kldoghpdblpjbjeechcaoibpfbgfomkn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers JSON-formatted CLI output for parsing and should request confirmation before account write actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
