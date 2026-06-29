## Description: <br>
Persistent cross-session memory for your agent, powered by HMR (Hestia Memory Runtime). Save important facts and preferences, recall relevant context, and restore cognitive state across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snowfoxhq](https://clawhub.ai/user/snowfoxhq) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to give an OpenClaw agent durable local memory for user preferences, important facts, decisions, task state, and later recall across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-term memory can retain sensitive or unwanted personal context across sessions. <br>
Mitigation: Save only user-approved durable facts, preferences, decisions, or task state; avoid saving secrets, passwords, API keys, or unnecessary personal data. <br>
Risk: Untrusted third-party content saved into memory can influence future agent behavior. <br>
Mitigation: Do not save scraped web pages, third-party messages, or other untrusted external content into long-term memory. <br>
Risk: Pointing the memory service at an untrusted remote endpoint could expose memory contents or alter recall behavior. <br>
Mitigation: Keep the HMR service bound to localhost and do not point HMR_BASE_URL at an untrusted remote server. <br>


## Reference(s): <br>
- [HMR Memory on ClawHub](https://clawhub.ai/snowfoxhq/hmr-memory) <br>
- [HMR project homepage](https://github.com/snowfoxHQ/HMR) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with local HTTP request examples and concise text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local HMR service on http://127.0.0.1:8077; optional HMR_TOKEN authentication is configured outside chat.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
