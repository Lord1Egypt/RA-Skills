## Description:

Metal Price automates login to qqthj.com, retrieves current metal price table data for selected ferroalloy categories, and exports the results to Excel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiang2023](https://clawhub.ai/user/wangxiang2023)

### License/Terms of Use:


## Use Case:

External users and market analysts use this skill to retrieve metal market price tables from qqthj.com for selected ferroalloy categories and export the data for spreadsheet review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation includes apparent account credentials.

Mitigation: Remove distributed credentials, rotate the exposed password if real, and provide credentials securely at runtime.

Risk: The skill mandates writing Excel exports to a fixed local Desktop path.

Mitigation: Confirm the export destination and overwrite behavior before allowing the skill to write files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangxiang2023/skills/metal-price)
- [qqthj.com](https://www.qqthj.com)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell command use and Excel file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports price table data to .xlsx files; the skill documentation specifies a fixed local Desktop export path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
