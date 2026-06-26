## Description: <br>
Eventee lets an agent search and read Eventee event data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent retrieve Eventee event content, attendee groups, participants, registrations, and session reviews through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Eventee account and may access event, attendee, registration, and review data. <br>
Mitigation: Use it only with the intended Eventee connection and handle returned data according to the event owner's access and privacy requirements. <br>
Risk: Connector action schemas can change, which can make stale payload assumptions incorrect. <br>
Mitigation: Inspect the live connector schema before each action and build payloads from that schema. <br>
Risk: First-time setup can install the oo CLI, start authentication, or direct the user to billing and connection pages. <br>
Mitigation: Run setup steps only after the matching command failure and only for the user's intended OOMOL account. <br>


## Reference(s): <br>
- [Eventee ClawHub skill page](https://clawhub.ai/oomol/oo-eventee) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Eventee homepage](https://eventee.co) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with oo CLI commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
