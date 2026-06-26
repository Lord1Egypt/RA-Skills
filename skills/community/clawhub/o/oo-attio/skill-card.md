## Description: <br>
Attio (attio.com). Use this skill for Attio requests that read, create, update, upsert, or delete records through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent work with Attio data through the OOMOL `oo` CLI, including schema inspection, record reads, record writes, upserts, and confirmed deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, and upsert Attio records when connected credentials are available. <br>
Mitigation: Inspect the live action schema and confirm the exact payload and expected effect with the user before running write actions. <br>
Risk: The skill can delete Attio records. <br>
Mitigation: Require explicit user approval for the target object and record ID before running destructive actions. <br>
Risk: The skill operates through an OOMOL-connected Attio account with sensitive credentials handled by the connector. <br>
Mitigation: Install only when the user intends agent access to Attio, and use the connected account with the minimum scopes needed for the task. <br>


## Reference(s): <br>
- [Attio homepage](https://attio.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub Attio skill](https://clawhub.ai/oomol/oo-attio) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [State-changing actions require user confirmation before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
