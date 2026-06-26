## Description: <br>
Telegram Bot (core.telegram.org) enables an agent to read, create, update, and delete Telegram Bot data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect Telegram bot state, send and manage messages, configure webhooks, and perform bot administration through approved OOMOL CLI actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Telegram Bot credential managed through OOMOL. <br>
Mitigation: Install and use it only when the user trusts OOMOL with the Telegram Bot connection, and avoid login or connection setup unless the user intentionally wants this environment connected. <br>
Risk: Confirmed write and destructive actions can post, edit, configure webhooks, create invite links, or delete bot-accessible messages. <br>
Mitigation: Review the exact action, target, and JSON payload with the user before approving write or destructive commands. <br>
Risk: Some history and update polling behavior depends on webhook delivery being disabled. <br>
Mitigation: Check webhook status and explain the delivery requirement before using polling-based chat history or update actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-telegram) <br>
- [Telegram Bot documentation](https://core.telegram.org/bots) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses from connector runs are JSON objects containing data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
