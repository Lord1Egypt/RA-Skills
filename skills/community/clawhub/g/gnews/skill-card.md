## Description: <br>
Use this skill when the user wants to install, configure, or troubleshoot the GNews binary from GitHub and fetch top headlines from GNews by country, category, and max article count. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ParinLL](https://clawhub.ai/user/ParinLL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CLI users use this skill to install and configure the GNews CLI, set the required GNEWS_API_KEY, run filtered headline requests, and troubleshoot API key, permission, and network failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a GNEWS_API_KEY and debug or troubleshooting output may expose sensitive operational context. <br>
Mitigation: Keep API keys private, avoid sharing debug output, and redact credentials in logs and support requests. <br>
Risk: The skill directs users to build and run code from a linked GitHub repository, with an optional sudo install for system-wide use. <br>
Mitigation: Review and trust the linked repository before building or running it, and use the optional sudo install only when a global binary is needed. <br>
Risk: The CLI depends on network access to gnews.io and returns external news API content. <br>
Mitigation: Treat API responses as untrusted input and verify network, firewall, proxy, quota, and credential issues during troubleshooting. <br>


## Reference(s): <br>
- [GNews API Go Client Repository](https://github.com/ParinLL/gnewsapi-go-client) <br>
- [GNews CLI on ClawHub](https://clawhub.ai/ParinLL/gnews) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include installation, environment-variable setup, CLI flag usage, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
