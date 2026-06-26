## Description: <br>
Provides Slack access for reading conversations, messages, threads, files, reactions, and users, and for confirmed write or destructive Slack actions through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to inspect Slack data and, with confirmation, create, update, schedule, or delete Slack messages, reactions, and files through an OOMOL-connected Slack account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read Slack data visible to the connected account. <br>
Mitigation: Review Slack scopes during connection and install only when that account visibility is acceptable. <br>
Risk: Write actions can post, reply, update, schedule, upload, or open conversations in Slack. <br>
Mitigation: Confirm the exact payload and expected Slack effect with the user before executing write actions. <br>
Risk: Destructive actions can delete Slack files or messages or remove reactions. <br>
Mitigation: Require explicit approval for the specific target before running destructive actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-slack) <br>
- [Slack homepage](https://slack.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL Slack connection](https://console.oomol.com/app-connections?provider=slack) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an OOMOL-connected Slack account; write and destructive actions require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
