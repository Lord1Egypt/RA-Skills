## Description: <br>
Pilot Group Chat helps agents coordinate multi-party conversations and group membership over the Pilot Protocol network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run group discussions, collaborative brainstorming, and team coordination among three or more agents. It is intended for environments where Pilot Protocol peers, trust relationships, and the pilotctl binary are already configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages and membership discovery are networked through Pilot peers, so sensitive content may be exposed to group participants or daemon configuration. <br>
Mitigation: Avoid sending secrets or sensitive operational details unless the group, peers, and Pilot daemon configuration are trusted. <br>
Risk: The skill proposes shell commands for group chat workflows. <br>
Mitigation: Review commands and target hostnames before execution, and confirm pilotctl, the daemon, and peer trust relationships are configured as expected. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-group-chat) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use pilotctl JSON mode and depend on an existing Pilot daemon, reachable peers, and trust relationships.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; SKILL.md metadata version 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
