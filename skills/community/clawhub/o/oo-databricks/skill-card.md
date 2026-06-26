## Description: <br>
This skill lets agents operate Databricks through OOMOL-connected oo CLI actions for reading, creating, updating, and deleting Databricks resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace operators use this skill to inspect Databricks schemas and run OOMOL-connected Databricks actions for jobs, clusters, repositories, secret scopes, and workspace files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, start, trigger, cancel, overwrite, or delete Databricks resources and workspace files. <br>
Mitigation: Require explicit user approval for every state-changing action and confirm the exact payload, target resource, and expected effect before execution. <br>
Risk: The skill requires an OOMOL-connected Databricks account with sensitive workspace credentials. <br>
Mitigation: Use least-privileged Databricks access and keep credentials in the OOMOL connection rather than exposing raw tokens in prompts or files. <br>
Risk: First-time setup may install or invoke the external oo CLI. <br>
Mitigation: Review the oo CLI installer before running it and only perform setup when an auth, connection, or missing-command error requires it. <br>


## Reference(s): <br>
- [Databricks](https://www.databricks.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-databricks) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads or results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the oo CLI to execute Databricks connector actions; state-changing and destructive actions require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
