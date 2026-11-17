## Description:

Collects model vendor and code tool pricing pages, helps fill pricing extraction JSON, and syncs the resulting data to a Feishu/Lark spreadsheet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sapereaude2014](https://clawhub.ai/user/sapereaude2014)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to collect official pricing pages, maintain target model and subscription plan tables, produce pricing JSON and CSV artifacts, and publish the data to Feishu/Lark Sheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates vendor pricing page collection, including concealed browser automation.

Mitigation: Review the configured source URLs before collection, run only against approved sources, and confirm that collection complies with site terms and organizational policy.

Risk: The push workflow can upload generated pricing data and replace managed Feishu/Lark spreadsheet tabs.

Mitigation: Use a least-privileged Lark identity, verify the target spreadsheet or folder, and review generated CSV contents before pushing.

Risk: Running the workflow in a broad environment could expose unrelated credentials to the collection and sync process.

Mitigation: Run in an isolated environment, avoid unrelated secrets, and pin or review dependencies before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sapereaude2014/skills/model-pricing-sync)
- [Configured vendor pricing sources](artifact/config/vendors.csv)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, JSON, CSV files, Configuration]

**Output Format:** [Markdown instructions with bash commands; generated Markdown page captures, JSON extraction files, and CSV tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can push generated CSV tables to Feishu/Lark Sheets after user review]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
