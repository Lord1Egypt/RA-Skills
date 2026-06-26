## Description: <br>
Retrieves Amazon Ads reports for Sponsored Products, Sponsored Brands, and Sponsored Display by creating, polling, downloading, and extracting report data for agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, operators, and developers use this skill to request Amazon Ads performance reports, choose report types and columns from bundled references, and receive downloaded structured report data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Amazon Ads authorization and can access downloaded business reports. <br>
Mitigation: Install and run it only in contexts where access to Amazon Ads credentials and report data is appropriate. <br>
Risk: Downloaded reports can be exposed through a temporary localhost HTTP link. <br>
Mitigation: Keep report serving bound to 127.0.0.1, disable HTTP serving when not needed, avoid sharing generated links, and delete report files after use. <br>
Risk: Automatic feedback reporting could include sensitive details if the agent sends raw user or report content. <br>
Mitigation: Do not include tokens, account IDs, report contents, local file paths, or other sensitive details in feedback submissions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-amazon-ads-report) <br>
- [Runtime Parameters and Field Reference](references/api.md) <br>
- [Report Types Index](references/report-types/index.md) <br>
- [Amazon Ads Reporting API Report Types](https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types) <br>
- [Amazon Ads Reporting API Reports Endpoint](https://advertising-api.amazon.com/reporting/reports) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON report results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return local file paths, file URIs, temporary localhost download links, report identifiers, and resume parameters for long-running reports.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
