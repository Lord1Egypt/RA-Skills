## Description: <br>
Zendesk skill for reading, creating, and updating Zendesk data through the OOMOL `oo` CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and support teams use this skill to list, inspect, create, reply to, and update Zendesk tickets, users, and organizations from an agent session through their connected OOMOL account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Zendesk credentials through an OOMOL-connected account. <br>
Mitigation: Use the server-side OOMOL credential flow and avoid handling raw Zendesk tokens in the agent session. <br>
Risk: Write actions can create tickets, add replies, or update existing Zendesk records. <br>
Mitigation: Confirm the exact payload and intended effect with the user before running any action tagged as write. <br>
Risk: Connector payload schemas may change or differ by connected account. <br>
Mitigation: Inspect the live action schema with `oo connector schema` before constructing each payload. <br>


## Reference(s): <br>
- [Zendesk homepage](https://www.zendesk.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL Zendesk connection page](https://console.oomol.com/app-connections?provider=zendesk) <br>
- [ClawHub skill listing](https://clawhub.ai/oomol/oo-zendesk) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OOMOL-connected Zendesk account; write actions require user confirmation before changing Zendesk state.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
