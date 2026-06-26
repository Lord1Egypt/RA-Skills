## Description: <br>
Installs the HeyCube personal profile management service for OpenClaw, including GET_CONFIG and UPDATE_DATA hook skills, a local SQLite management tool, and configuration edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MMMMMMTL](https://clawhub.ai/user/MMMMMMTL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install a HeyCube memory layer that loads user profile context before conversations and updates local profile data after qualifying conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installed hooks can process future conversations and update a persistent local profile store. <br>
Mitigation: Review the AGENTS.md hook rules before enabling the skill, use the .heycube-off switch when profile processing is not desired, and remove the hook skill directories when decommissioning it. <br>
Risk: Redacted conversation summaries may be sent to HeyCube after an API key is configured. <br>
Mitigation: Configure the API key only after approving this data-sharing behavior, review TOOLS.md, and keep the documented redaction rules in place. <br>
Risk: Personal profile data persists in a local SQLite database. <br>
Mitigation: Store the database in an appropriate workspace, inspect it with the provided get-all command when needed, and delete personal-db.sqlite when the memory layer is no longer required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MMMMMMTL/heycube-setup) <br>
- [HeyCube service](https://heifangti.com) <br>
- [HeyCube API endpoint](https://heifangti.com/api/api/v1/heifangti) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline PowerShell, Bash, JSON, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installation and verification steps for hook skills, local SQLite tooling, and OpenClaw configuration files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
