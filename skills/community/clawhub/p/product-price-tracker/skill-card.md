## Description: <br>
Tracks product price changes, compares them with local price history, and generates monitoring reports for competitive pricing, discount alerts, and trend analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rf-ai-wh](https://clawhub.ai/user/rf-ai-wh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and business users can use this skill to track product and competitor prices, record price observations, and generate reports that summarize current prices and historical changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product names and search terms may be sent to a search tool during price lookup. <br>
Mitigation: Use only approved product terms and avoid sensitive business data unless the configured search tool is approved for that data. <br>
Risk: Default storage paths use /tmp, which may be ephemeral or inappropriate for sensitive monitoring data. <br>
Mitigation: Set PRICE_DB_FILE and PRICE_SCREENSHOT_DIR to a private persistent location before operational use. <br>
Risk: The cron example can create ongoing scheduled report runs. <br>
Mitigation: Enable scheduled execution only after reviewing the command, storage paths, and reporting expectations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rf-ai-wh/product-price-tracker) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, plain-text CLI output, and local JSON records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local price history data and optional screenshot directories when the Python CLI is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
