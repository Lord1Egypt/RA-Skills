## Description: <br>
Provides read-only inspection of Apache Airflow DAGs, DAG runs, and task instances through the Airflow REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kansodata](https://clawhub.ai/user/kansodata) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Airflow operators use this skill to inspect DAG inventories, recent DAG runs, and task instances without changing Airflow state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The external Airflow plugin and credential permissions determine the real operational impact. <br>
Mitigation: Use an Airflow credential limited to read-only API access and install only when the referenced plugin is trusted. <br>
Risk: The skill requires valid host configuration and authentication to inspect Airflow. <br>
Mitigation: Report missing configuration or authentication errors explicitly instead of inventing values or assuming Airflow state. <br>
Risk: Accidental mutation requests would exceed the intended scope. <br>
Mitigation: Use only the listed read-only tools and decline trigger, pause, delete, patch, update, or other state-changing actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kansodata/kansodata-airflow-readonly) <br>
- [kansodata publisher profile](https://clawhub.ai/user/kansodata) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, api calls, guidance] <br>
**Output Format:** [Concise Markdown summaries with exact Airflow identifiers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only responses should report missing configuration, authentication errors, or empty results explicitly.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
