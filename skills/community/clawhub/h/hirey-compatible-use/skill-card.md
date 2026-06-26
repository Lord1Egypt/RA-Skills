## Description: <br>
Uses an already-installed Hi service on OpenClaw to help agents publish people-finding listings, find and assess matches, contact promising people, and coordinate meetings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yzlee](https://clawhub.ai/user/yzlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and their agents use this skill after Hi is installed to manage people-to-people matching workflows, including job and hiring searches, housing or social matching, outreach, pairings, and meeting coordination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may automatically apply Hi plugin updates and restart the OpenClaw gateway from release events without asking the owner first. <br>
Mitigation: Require explicit approval for plugin installs, restarts, and rollbacks, or delegate those actions to a separate trusted updater. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yzlee/hirey-compatible-use) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with tool-use instructions and occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Directs the agent to use Hi tools for listings, matching sessions, pairings, meetings, health checks, and release handling.] <br>

## Skill Version(s): <br>
0.1.61 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
