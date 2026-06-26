## Description: <br>
Remember The Milk skill for OpenClaw <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kissyjpf](https://clawhub.ai/user/kissyjpf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agents use this skill to manage Remember The Milk tasks from a command-line style interface, including listing, creating, editing, completing, and deleting tasks after account authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests delete-level access to the user's Remember The Milk account and can complete, edit, or delete tasks. <br>
Mitigation: Install only when delete-level task access is acceptable, and double-check persistent task IDs before running edit, complete, or delete commands. <br>
Risk: API credentials and authorization tokens are stored locally in user-accessible files. <br>
Mitigation: Keep ~/.rtm-credentials.json, ~/.rtm-token.json, and any .env file private, and avoid syncing or committing those files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kissyjpf/openclaw-rtm) <br>
- [Remember The Milk](https://www.rememberthemilk.com/) <br>
- [Remember The Milk API keys](https://www.rememberthemilk.com/services/api/keys.rtm) <br>
- [Remember The Milk REST API endpoint](https://api.rememberthemilk.com/services/rest/) <br>
- [Remember The Milk authorization endpoint](https://www.rememberthemilk.com/services/auth/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown-style command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include task IDs, task metadata, authorization URLs, credential setup instructions, and status messages from Remember The Milk operations.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
