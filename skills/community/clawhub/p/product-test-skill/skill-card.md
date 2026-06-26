## Description: <br>
Processes CSV files to generate statistical summaries for numeric columns and row counts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aidfsoft](https://clawhub.ai/user/aidfsoft) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data practitioners use this skill to inspect local CSV files and produce basic descriptive statistics for selected numeric columns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-selected local CSV files, which may contain sensitive or regulated data. <br>
Mitigation: Use only approved files and limit selected columns to data that may be processed in the target environment. <br>
Risk: The release evidence notes stale or mismatched metadata, so the catalog summary may not fully match the shipped artifact. <br>
Mitigation: Review the actual skill documentation and expected CSV behavior before installation or use. <br>
Risk: Statistical summaries can be misleading when columns contain malformed, missing, or non-representative data. <br>
Mitigation: Validate input columns and review summary outputs before using them for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aidfsoft/product-test-skill) <br>
- [Skill documentation](artifact/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON] <br>
**Output Format:** [JSON statistical summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes per-column mean, median, standard deviation, minimum, maximum, and row count for local CSV inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
