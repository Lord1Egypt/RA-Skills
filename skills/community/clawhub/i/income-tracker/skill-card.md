## Description: <br>
Income Tracker records multi-source income, summarizes earnings, and generates trend and source analysis for freelancers, creators, side businesses, and small teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users such as freelancers, creators, side-business operators, and small teams use this skill to record income, review period summaries, analyze income sources, view trends, and export selected records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Income records, backups, and exports may contain sensitive financial data. <br>
Mitigation: Set DATA_PATH to a private location, restrict file permissions, protect backups and exports, and encrypt storage when handling sensitive records. <br>
Risk: Dependency lock data references non-HTTPS package mirror URLs. <br>
Mitigation: Reinstall dependencies from a trusted HTTPS registry before deployment when supply-chain assurance is required. <br>
Risk: The skill writes local files when recording income. <br>
Mitigation: Invoke the skill explicitly and review the configured DATA_PATH before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/income-tracker) <br>
- [Clawdis homepage](https://clawhub.com/skills/income-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Analysis, Configuration, Files] <br>
**Output Format:** [JSON objects with plain text messages, ASCII charts, and CSV or JSON export payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local JSON income records to DATA_PATH and may return exported records as CSV or JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, frontmatter, package.json, skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
