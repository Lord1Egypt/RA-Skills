## Description: <br>
OneSignal (onesignal.com). Use this skill for ANY OneSignal request: reading, creating, and updating data through the OOMOL OneSignal connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect OneSignal action schemas, list or retrieve messages, create push notifications, and cancel scheduled messages through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create push notifications or cancel scheduled OneSignal messages when those actions are run. <br>
Mitigation: Review and explicitly approve write-action payloads and intended effects before execution. <br>
Risk: The connected OneSignal credentials are held server-side by OOMOL. <br>
Mitigation: Install only when the user wants an agent to operate the connected OneSignal app through OOMOL. <br>


## Reference(s): <br>
- [OneSignal homepage](https://onesignal.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-onesignal-rest-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
