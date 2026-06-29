## Description: <br>
OnceHub helps agents search and read booking pages, bookings, and event types through an OOMOL-connected OnceHub account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to retrieve OnceHub booking pages, bookings, and event types from an OOMOL-connected OnceHub account. The skill supports booking lookup workflows, including last-update filtering where the live connector schema allows it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on OOMOL as the broker for the user's OnceHub account. <br>
Mitigation: Install and use it only when OOMOL is an acceptable broker for the account and organization. <br>
Risk: The first-time setup path includes shell-based oo CLI installation commands. <br>
Mitigation: Review installation commands before execution and use official installation guidance appropriate for the user's platform. <br>
Risk: Future connector actions may include write or destructive operations even though this release lists only read actions. <br>
Mitigation: Keep use to listed read-only actions unless a future version clearly documents write actions and the user explicitly confirms the payload and effect. <br>
Risk: Connector input and output schemas may change over time. <br>
Mitigation: Inspect the live connector schema before constructing each action payload. <br>


## Reference(s): <br>
- [OnceHub homepage](https://www.oncehub.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-oncehub) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before action payload construction; action responses are JSON from the oo CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release, artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
