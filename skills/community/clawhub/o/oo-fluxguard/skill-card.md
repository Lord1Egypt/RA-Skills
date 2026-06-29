## Description: <br>
Fluxguard (fluxguard.com). Use this skill for ANY Fluxguard request - reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Fluxguard monitoring through the OOMOL oo CLI connector, including account reads, page and category management, crawls, and webhook administration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write or destructive Fluxguard actions can create, change, or delete monitored pages, sites, categories, webhooks, or account data. <br>
Mitigation: Confirm the exact payload, target, and expected effect with the user before any write action, and require explicit approval before destructive actions. <br>
Risk: Overbroad or stale Fluxguard credentials could expose more account access than the task requires. <br>
Mitigation: Use the least-privileged Fluxguard credential available and reconnect only when the connector reports a missing, expired, or not-ready credential. <br>
Risk: Connector input fields can drift from the skill text and cause incorrect requests. <br>
Mitigation: Inspect the live connector schema before constructing each action payload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-fluxguard) <br>
- [Fluxguard homepage](https://fluxguard.com/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses oo CLI connector actions; write and destructive actions require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill metadata and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
