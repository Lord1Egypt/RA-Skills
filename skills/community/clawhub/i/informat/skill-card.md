## Description: <br>
Informat helps agents administer Informat platform workspaces by reading method parameter references, querying existing application structure, and issuing documented system method calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[informat365](https://clawhub.ai/user/informat365) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace administrators use this skill to inspect and manage Informat applications, tables, dashboards, automations, workflows, scripts, and records through documented system methods. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad live-system administration powers when configured with an Informat agent token. <br>
Mitigation: Use a least-privilege token, scope access to the intended workspace, and avoid production applications unless the action is necessary and approved. <br>
Risk: Deletes, publishing, bulk record changes, script execution, JavaScript evaluation, outbound web requests, email, and notifications can have irreversible or external effects. <br>
Mitigation: Require human confirmation for those actions and review the exact method name, target app, and JSON parameters before execution. <br>
Risk: Incorrect IDs or field names can modify the wrong Informat object or cause failed operations. <br>
Mitigation: Follow the documented discovery flow: query existing structures, retrieve full field definitions, and read the matching parameter reference before any create or modify call. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/informat365/informat) <br>
- [Informat platform host](https://ai.ainformat.com/) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Method caller script](artifact/scripts/call.js) <br>
- [Application publish parameter reference](artifact/references/system_app_publish.json) <br>
- [JavaScript evaluation parameter reference](artifact/references/system_javascript_eval.json) <br>
- [Bulk record deletion parameter reference](artifact/references/system_table_record_batch_delete.json) <br>
- [System email parameter reference](artifact/references/system_send_system_email.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to create JSON parameter files and invoke the bundled Node.js caller against an Informat workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
