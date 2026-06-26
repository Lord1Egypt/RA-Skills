## Description: <br>
Consulta processos judiciais brasileiros (Brasil) via API Pública do DataJud (CNJ). <br>

This skill is for research and development only. <br>

## Publisher: <br>
[runawaydevil](https://clawhub.ai/user/runawaydevil) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to query public Brazilian court processes by CNJ number, search by court filters, infer tribunals, and monitor case updates through DataJud. <br>

### Deployment Geography for Use: <br>
Brazil <br>

## Known Risks and Mitigations: <br>
Risk: Court lookup queries are sent to CNJ's public DataJud API and may reveal legal research interests. <br>
Mitigation: Use the skill only for queries appropriate to send to DataJud and avoid entering sensitive case research unless that disclosure is acceptable. <br>
Risk: The monitoring state file can reveal which process numbers the user tracks. <br>
Mitigation: Protect or delete state/monitor.json when monitored cases are sensitive. <br>
Risk: Dry-run output can expose an Authorization header when a private DATAJUD_API_KEY is configured. <br>
Mitigation: Avoid dry-run with private API keys, and redact command output before sharing logs. <br>


## Reference(s): <br>
- [API Pública do DataJud (CNJ)](https://api-publica.datajud.cnj.jus.br/) <br>
- [ClawHub release page](https://clawhub.ai/runawaydevil/klaus-processos-br) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Plain text or JSON from CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can persist monitored process numbers and recent movement snapshots in state/monitor.json.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
