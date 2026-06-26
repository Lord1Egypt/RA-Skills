## Description: <br>
Downloads financial reports for A-share, Hong Kong, and U.S. stocks by identifying the market, selecting the appropriate scraper, and exporting JSON, CSV, and optional PDF files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cgxxxxxxxxxxxx](https://clawhub.ai/user/cgxxxxxxxxxxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and finance teams use this skill to collect annual, interim, quarterly, SEC 10-K/10-Q, and foreign issuer 20-F/6-K reports for target public companies across A-share, Hong Kong, and U.S. markets. <br>

### Deployment Geography for Use: <br>
Global, with workflows focused on China A-share, Hong Kong, and U.S. public-company filings. <br>

## Known Risks and Mitigations: <br>
Risk: The downloader shells out to external scraper scripts and depends on code outside this package. <br>
Mitigation: Review the referenced scraper scripts before installing or relying on the skill, and run --dry-run first to inspect intended behavior. <br>
Risk: User-provided stock and report-type values are passed into shell commands. <br>
Mitigation: Use ordinary stock codes and documented report types only, avoid custom --type values, and run the skill in a controlled workspace. <br>
Risk: The documentation suggests creating an optional global /usr/local/bin helper. <br>
Mitigation: Create the helper only when a global command is deliberately needed and the referenced script path is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cgxxxxxxxxxxxx/global-financial-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, Python invocation examples, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloader commands may write JSON, CSV, and optional PDF files under OpenClaw workspace export or archive directories.] <br>

## Skill Version(s): <br>
2.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
