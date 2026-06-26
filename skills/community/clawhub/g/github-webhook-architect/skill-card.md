## Description: <br>
Guides users through configuring OpenClaw, Nginx, and GitHub Actions to establish a secure, autonomous GitHub integration pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patello](https://clawhub.ai/user/patello) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to plan an OpenClaw webhook integration that routes GitHub events through Nginx and GitHub Actions. It helps them configure request payloads, secrets, session grouping, HTTPS enforcement, and agent authorization before repository events trigger an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Externally triggered GitHub events can cause an agent to act with broad GitHub authority. <br>
Mitigation: Use HTTPS only, least-privileged GitHub tokens and agents, narrow workflow triggers, verified actor checks from signed GitHub webhook or API data, an allowlisted command schema, and human approval before repository-writing actions. <br>
Risk: Automated server or reverse-proxy configuration can override existing routing or expose a local OpenClaw gateway. <br>
Mitigation: Require explicit authorization before making configuration changes, keep OpenClaw bound to 127.0.0.1, review Nginx and OpenClaw config before applying it, and test only the intended mapped hook path. <br>
Risk: HTTP testing can expose authorization tokens in transit. <br>
Mitigation: Prefer HTTPS from the start; if HTTP testing is used, disable the HTTP route, rotate the OpenClaw hook token, update GitHub Secrets, and move immediately to HTTPS. <br>


## Reference(s): <br>
- [Github Webhook Architect on ClawHub](https://clawhub.ai/patello/github-webhook-architect) <br>
- [patello publisher profile](https://clawhub.ai/user/patello) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, YAML, Nginx, AGENTS.md, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include optional file edits or command suggestions only after explicit user authorization.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence; artifact metadata reports 1.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
