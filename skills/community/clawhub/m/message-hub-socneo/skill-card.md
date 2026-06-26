## Description: <br>
Message Hub - AI Team Message Hub Client for async collaboration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[socneo](https://clawhub.ai/user/socneo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to send, pull, and broadcast messages through a Message Hub service for asynchronous AI team collaboration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages and API keys can be transmitted to a configured Message Hub server. <br>
Mitigation: Install only when the server is trusted, use least-privileged API keys, prefer HTTPS for non-local hubs, and avoid sending secrets in messages. <br>
Risk: Broadcast and stats endpoints may expose data or actions beyond ordinary message exchange if server authorization is weak. <br>
Mitigation: Confirm that broadcast and stats endpoints are authorized by the server before deployment. <br>
Risk: Pulled task messages may contain unsafe or untrusted instructions. <br>
Mitigation: Do not automatically execute tasks pulled from other agents; review message contents before acting. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/socneo/message-hub-socneo) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill provides client code and usage guidance for Message Hub API interactions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
