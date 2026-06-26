## Description: <br>
Inspects container health and suggests fixes for common errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liverock](https://clawhub.ai/user/liverock) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Docker Medic to inspect Docker container health, identify common log or status patterns, and get suggested remediation actions for affected containers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Container health recommendations may be incomplete or not fit a specific production environment. <br>
Mitigation: Review the reported diagnosis and suggested remediation against live Docker logs, service dependencies, and deployment policy before making changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liverock/openclaw-skill-local-docker-health-check) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Plain-text summary, Markdown status table, and JSON prescriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May target a named container or inspect all containers; suggested fixes should be reviewed before operational changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
