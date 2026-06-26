## Description: <br>
Systematic workflow to locate and verify the Mission Control SQLite database when path assumptions fail, and reconcile frontend/backend schema mismatches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guillaumemaka](https://clawhub.ai/user/guillaumemaka) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to find the actual Mission Control SQLite database path, confirm the database and schema, and resolve frontend/backend task column mismatches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SQLite inspection commands may display local Mission Control task contents. <br>
Mitigation: Run the commands only in the intended project environment and avoid sharing query output that contains local task data. <br>
Risk: Assuming the wrong database path or task column name can lead to incorrect troubleshooting conclusions. <br>
Mitigation: Trace the database creation path and inspect the live schema before changing frontend types or backend code. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown checklist with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only local SQLite inspection workflow; no API keys or network calls indicated.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
