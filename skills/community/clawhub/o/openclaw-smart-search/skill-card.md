## Description: <br>
Openclaw Smart Search is a CLI skill that routes search queries across Bailian MCP, Tavily, Serper, Exa, and Firecrawl, then merges and ranks the results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fdenny11gg](https://clawhub.ai/user/fdenny11gg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run web, academic, technical, news, and crawl-oriented searches from the command line while the skill selects available providers and merges results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary flags unsafe credential setup and display paths. <br>
Mitigation: Review or remove quick-config.sh before use, provide your own provider API keys, and avoid key display or status commands in shared terminals or logs. <br>
Risk: Search queries and crawl targets may be sent to third-party providers. <br>
Mitigation: Do not submit confidential data as search input unless the selected providers and account terms are approved for that data. <br>
Risk: OPENCLAW_MASTER_KEY protects encrypted provider credentials. <br>
Mitigation: Treat OPENCLAW_MASTER_KEY like a password and prefer a secret manager or tightly permissioned file over plaintext .env or shell-profile storage. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fdenny11gg/openclaw-smart-search) <br>
- [Node.js child process security guidance](https://nodejs.org/en/docs/guides/security/#child-processes) <br>
- [OWASP Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text CLI output with search-result summaries, source links, engine status, and setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search behavior depends on configured provider API keys, OPENCLAW_MASTER_KEY, node, and mcporter availability.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release evidence and package.json; changelog top entry is 1.0.12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
