## Description: <br>
Manage Kibana Data Views, formerly index patterns, via REST API for creating, listing, updating, deleting, checking existence, and troubleshooting missing index patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chunkin616-hue](https://clawhub.ai/user/chunkin616-hue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and observability engineers use this skill to manage Kibana data views and repair missing or corrupted index-pattern references before building or restoring dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform live administrative Kibana changes, including delete, cleanup, and recreate operations for data views. <br>
Mitigation: Require explicit human confirmation before destructive operations, run dry-run modes first where available, and export or back up affected Kibana saved objects before changes. <br>
Risk: The artifact includes hardcoded local host guidance and credential examples that may be unsafe if reused directly. <br>
Mitigation: Replace hardcoded hosts and sample credentials before use, prefer HTTPS, and use scoped credentials with the minimum required Kibana permissions. <br>
Risk: Troubleshooting guidance can involve kubectl and direct Elasticsearch queries against observability infrastructure. <br>
Mitigation: Limit these actions to authorized operators and require review before running kubectl or direct Elasticsearch commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chunkin616-hue/kibana-data-views) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with REST examples and Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or run Kibana REST API operations that list, create, delete, clean up, or recreate data views.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
