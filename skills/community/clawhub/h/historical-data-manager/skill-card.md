## Description: <br>
Extract, clean, and organize legacy construction data from archives. Migrate historical project data, cost records, and schedules into modern formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Construction data teams, estimators, schedulers, and developers use this skill to process local legacy archives, normalize historical project records, and prepare structured outputs for benchmarking, estimating calibration, and analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read local construction archives and legacy database files selected by the user. <br>
Mitigation: Limit the agent to a specific archive folder and verify spreadsheet or database paths before processing. <br>
Risk: Generated exports could be written to unintended locations or with unclear filenames. <br>
Mitigation: Review output filenames and destinations before allowing writes. <br>
Risk: The skill may encounter unrelated private files if pointed at a broad directory. <br>
Mitigation: Avoid granting access to unrelated private directories and scope processing to the intended project archive. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/datadrivenconstruction/historical-data-manager) <br>
- [Publisher Profile](https://clawhub.ai/user/datadrivenconstruction) <br>
- [Project Homepage](https://datadrivenconstruction.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured tables, Python examples, and optional export guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Excel, CSV, or JSON exports for user-selected construction data.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
