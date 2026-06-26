## Description: <br>
Refiner (refiner.io). Use this skill for ANY Refiner request - reading, creating, updating, and deleting data. Whenever a task involves Refiner, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate a connected Refiner workspace through OOMOL, including contact, form, segment, response, reporting, account, and event workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use sensitive Refiner credentials through an OOMOL-connected account. <br>
Mitigation: Install only when the agent should operate that Refiner workspace, and use the OOMOL connection flow only if that provider is trusted. <br>
Risk: Some connector actions can create, update, remove, or otherwise change Refiner data. <br>
Mitigation: Review payloads and effects before approving write actions, and require explicit approval before destructive actions. <br>
Risk: Connector schemas may change over time, which can make cached payload assumptions inaccurate. <br>
Mitigation: Inspect the live connector schema before constructing each action payload. <br>


## Reference(s): <br>
- [ClawHub Refiner skill](https://clawhub.ai/oomol/oo-refiner) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Refiner homepage](https://refiner.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill directs agents to inspect live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
