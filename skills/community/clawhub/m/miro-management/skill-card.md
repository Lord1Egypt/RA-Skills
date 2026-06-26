## Description: <br>
Manage Miro through the Miro REST API using OAuth 2.0, saved token files, or direct access tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect a personal or local Miro integration, inspect boards and members, create or update board content, manage webhooks, export board data, and preview or send Miro REST API requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses powerful Miro API credentials that can read, write, delete, manage webhooks, and send raw API requests depending on token permissions. <br>
Mitigation: Use a least-privilege Miro app or token, test on noncritical boards first, and explicitly approve every write, delete, webhook, or raw API request. <br>
Risk: OAuth flows and saved token files can expose client secrets, access tokens, or refresh tokens if terminal output or local files are shared. <br>
Mitigation: Keep secrets outside the skill package, avoid running OAuth flows where terminal output is captured in shared logs or chat, and protect or rotate any saved .miro/tokens.json file. <br>


## Reference(s): <br>
- [Miro OAuth notes](references/miro-oauth-notes.md) <br>
- [Miro request examples](references/miro-request-examples.md) <br>
- [Miro OAuth authorization endpoint](https://miro.com/oauth/authorize) <br>
- [Miro OAuth token endpoint](https://api.miro.com/v1/oauth/token) <br>
- [Miro REST API base](https://api.miro.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON, CSV, or Markdown export files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide Miro API calls that read or write local token files and mutate live Miro boards when the user runs the generated commands.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
