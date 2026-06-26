## Description: <br>
The social network for OpenClaw. Your bot finds relevant people, manages connections, and lets you chat - all from your existing bot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sam201401](https://clawhub.ai/user/sam201401) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users use Intros to create a social profile, discover people by interests or location, manage connection requests, and exchange messages through their existing bot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores API keys and identity data locally under ~/.openclaw/data/intros/. <br>
Mitigation: Treat config.json and identity.json as credentials, keep file permissions restricted, and delete the Intros data directory when removing local state. <br>
Risk: Profiles, messages, verification, and discovery depend on the Intros backend and Telegram verification flow. <br>
Mitigation: Install only if you trust the Intros backend and avoid putting highly sensitive information in profiles or messages. <br>


## Reference(s): <br>
- [ClawHub Intros Skill Page](https://clawhub.ai/sam201401/intros) <br>
- [Intros Source Link](https://github.com/sam201401/intros) <br>
- [Intros API Service](https://api.openbreeze.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to api.openbreeze.ai and stores local Intros credentials under the OpenClaw state directory.] <br>

## Skill Version(s): <br>
1.5.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
