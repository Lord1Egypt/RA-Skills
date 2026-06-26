## Description: <br>
Retrieve timely, authoritative financial news, announcements, research reports, policies, and other finance-related information using the Meixiang search API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xpmars](https://clawhub.ai/user/xpmars) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and finance-focused agents use this skill to query current financial news, announcements, research reports, policy documents, trading rules, and event data through the Meixiang API. It is intended for finance-related questions where the user needs current source data rather than opinion-only analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user queries to a disclosed external Meixiang API and requires an API key. <br>
Mitigation: Use a dedicated API key when possible and avoid including secrets, account details, personal data, proprietary research, or nonpublic investment information in queries. <br>
Risk: Saved raw JSON results may retain sensitive query context or financial research material. <br>
Mitigation: Save results only when needed and delete saved JSON files when they are no longer required. <br>


## Reference(s): <br>
- [Meixiang financial search API endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries with optional shell commands and JSON excerpts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save raw JSON results to the current work directory when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
