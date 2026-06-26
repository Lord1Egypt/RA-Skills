## Description: <br>
Operate Holded ERP through holdedcli to read and update data safely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaumecornado](https://clawhub.ai/user/jaumecornado) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and business users use this skill to read, search, create, update, or delete Holded ERP entities through holdedcli while validating actions and requiring explicit confirmation before writes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a Holded ERP account with powerful account access. <br>
Mitigation: Use the least-privileged Holded API key available and install only when the external holded CLI is trusted. <br>
Risk: Write, delete, accounting, or --skip-validation receipt actions could change business records if confirmed incorrectly. <br>
Mitigation: Review every proposed command and payload carefully, and only confirm changes that are fully understood. <br>


## Reference(s): <br>
- [Holded Skill ClawHub Page](https://clawhub.ai/jaumecornado/holded-skill) <br>
- [Holded Skill Homepage](https://github.com/jaumecornado/holded-skill) <br>
- [Holded CLI Reference](references/holdedcli-reference.md) <br>
- [Holded CLI](https://github.com/jaumecornado/holdedcli) <br>
- [Holded API Key Documentation](https://developers.holded.com/reference/api-key) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries include relevant IDs, HTTP status, API snippets, and applied changes when available.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
