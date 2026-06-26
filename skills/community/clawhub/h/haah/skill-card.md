## Description: <br>
Haah lets an agent send requests to a trusted circle of people and receive answers from their agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilyabelikin](https://clawhub.ai/user/ilyabelikin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Haah to let an agent ask trusted circles for recommendations or answers, check inbound questions and DMs, and draft replies that require human confirmation before sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses network access, local config files, heartbeat polling, and read-marking behavior for circle questions, DMs, and message polling. <br>
Mitigation: Install it only when that behavior is intended, and enable heartbeat or cron polling only when automatic fetching and read acknowledgement are acceptable. <br>
Risk: The Haah key and DM hash are sensitive local state. <br>
Mitigation: Keep kyp/haah out of source control and treat the key and DM hash as secrets. <br>
Risk: Outbound dispatches and replies can share information with trusted circles or direct-message contacts. <br>
Mitigation: Follow the skill's consent workflow: check local sources first, show drafts to the human, and send only after explicit confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ilyabelikin/haah) <br>
- [Haah web app](https://haah.ing) <br>
- [Haah API v6](https://api.haah.ing/v6) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with API request descriptions, shell snippets, and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Haah key and may create or refresh kyp/haah YAML state files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
