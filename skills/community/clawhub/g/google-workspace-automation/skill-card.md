## Description: <br>
Design Gmail, Drive, Sheets, and Calendar automations with scope-aware plans. Use for repeatable daily task automation with explicit OAuth scopes and audit-ready outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x-Professor](https://clawhub.ai/user/0x-Professor) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations teams use this skill to design repeatable Google Workspace automations for Gmail, Drive, Sheets, Calendar, and related services with explicit OAuth scopes and auditable planning artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The planner reads a user-supplied JSON requirements file and writes an output artifact, so sensitive input paths or important output paths can create exposure or overwrite risk. <br>
Mitigation: Use a dedicated project/output directory, avoid sensitive input files, and choose output paths where overwriting would not matter. <br>
Risk: Workspace automations can accumulate broader OAuth access when unrelated service actions are grouped together. <br>
Mitigation: Keep unrelated automations separate and request only the service scopes required by the declared actions. <br>


## Reference(s): <br>
- [Workspace Automation Guide](references/workspace-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON, Markdown, or CSV planning artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The local planner reads an optional JSON requirements file up to 1 MiB and writes the requested output artifact.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
