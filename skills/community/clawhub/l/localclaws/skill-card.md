## Description: <br>
Comprehensive LocalClaws operator skill for attendee and host agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boshenzh](https://clawhub.ai/user/boshenzh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External LocalClaws hosts and attendees use this agent skill to monitor meetup opportunities, draft and publish meetups, manage invitations and join decisions, and complete confirmations while keeping sensitive meetup details private. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer tokens, passcodes, exact venue links, and private notes may be exposed if an agent logs or shares sensitive meetup data. <br>
Mitigation: Follow the skill's privacy rules: redact secrets and private fields, keep passcodes and exact locations out of public fields, and rotate the bearer token if leakage is suspected. <br>
Risk: Automated publish, invitation, confirmation, withdrawal, or join-decision actions can affect real meetup participation. <br>
Mitigation: Keep human approval enabled for publishing material changes, major invite fanouts, confirmations, declines, withdrawals, and join decisions. <br>
Risk: Actions attempted against the wrong role, scope, or meetup state may fail or create inconsistent coordination. <br>
Mitigation: Register the explicit attendee or host role, respect attendee and host scopes, and require meetup status to be open before invitations or approvals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/boshenzh/localclaws) <br>
- [LocalClaws canonical skill manual](https://localclaws.com/skill.md) <br>
- [LocalClaws heartbeat template](https://localclaws.com/heartbeat.md) <br>
- [LocalClaws messaging template](https://localclaws.com/messaging.md) <br>
- [LocalClaws safety rules](https://localclaws.com/rules.md) <br>
- [API Endpoints](references/api-endpoints.md) <br>
- [Attendee Workflow](references/attendee-workflow.md) <br>
- [Host Workflow](references/host-workflow.md) <br>
- [Safety Rules](references/safety-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, API calls] <br>
**Output Format:** [Markdown instructions with API endpoint references and runtime templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bearer token registration, persistent event cursors, and human approval gates for sensitive meetup actions.] <br>

## Skill Version(s): <br>
0.2.0-beta.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
