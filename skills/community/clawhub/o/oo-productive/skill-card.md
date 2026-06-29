## Description: <br>
Productive enables agents to operate Productive through the OOMOL oo CLI for task and time-entry retrieval, creation, updates, and deletion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage Productive tasks and time entries through an OOMOL-connected account while relying on live action schemas for accurate payload construction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording can lead an agent to use the integration for many Productive requests, including business-data operations. <br>
Mitigation: Review the skill text before installation, use the narrowest Productive permissions available, and distinguish read-only requests from state-changing actions. <br>
Risk: Task and time-entry create, update, or delete actions can change or remove Productive data. <br>
Mitigation: Require explicit user confirmation of the target, payload, and expected effect before running write or destructive actions. <br>


## Reference(s): <br>
- [Productive homepage](https://productive.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Productive skill on ClawHub](https://clawhub.ai/oomol/skills/oo-productive) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live action schema inspection before constructing Productive action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
