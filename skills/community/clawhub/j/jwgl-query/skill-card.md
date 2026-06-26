## Description: <br>
Query teacher-facing JWGL systems for course schedules, invigilation duties, exam arrangements, and locally managed school and teacher account settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jovial-liu](https://clawhub.ai/user/jovial-liu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers, school staff, and supporting agents use this skill to query JWGL academic systems for weekly course schedules, invigilation duties, course exam arrangements, and exam information. Agents can also help manage local school URLs and teacher credentials needed for repeat queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Teacher-side JWGL usernames and passwords are stored locally in config.json. <br>
Mitigation: Keep config.json out of Git, backups, and shared folders; use a dedicated low-privilege account or secure secret storage where available. <br>
Risk: Debug and probe tools can save authenticated HTML pages and screenshots. <br>
Mitigation: Use debug or probe output only when needed for troubleshooting, store it locally, and delete captured output after review. <br>


## Reference(s): <br>
- [Config Format](references/config-format.md) <br>
- [Query Types](references/query-types.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jovial-liu/jwgl-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON query results from the runtime scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Query result JSON includes fields such as query_type, teacher, term, count, rows, and details for aggregated exam queries.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
