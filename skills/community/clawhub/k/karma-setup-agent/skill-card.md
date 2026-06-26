## Description: <br>
Set up or log in to Karma before first use of Karma skills, including API key creation, saving, and configuration verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maheshmurthy](https://clawhub.ai/user/maheshmurthy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent environment to Karma, obtain or enter a Karma API key, optionally persist it in shell configuration, and verify that the setup is ready for Karma project and funding workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill requires careful handling of a local Ziniao/ZClaw bridge with browser-control authority and a ZClaw API key. <br>
Mitigation: Install only when the local bridge is trusted, use a dedicated revocable API key, avoid pasting secrets into shared chats, keep local configuration private, and rotate the key if it appears in logs or transcripts. <br>
Risk: The skill asks users to handle Karma API keys that may be saved in shell configuration files. <br>
Mitigation: Ask permission before persisting secrets, avoid duplicate key entries, keep shell configuration files private, and prefer revocable keys. <br>


## Reference(s): <br>
- [Agent API Reference](../references/agent-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask the user for an email address, verification code, or API key during setup.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
