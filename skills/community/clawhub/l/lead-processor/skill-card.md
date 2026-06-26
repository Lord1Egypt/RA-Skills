## Description: <br>
Automates B2B lead cleaning and classification by analyzing client websites, grading leads A/B/C, updating Feishu tables, and sending reports to Feishu groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clonbrowser](https://clawhub.ai/user/clonbrowser) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales and business development teams use this skill to triage foreign-trade B2B leads from Feishu tables, classify prospects by fit, write structured lead assessments, and notify a Feishu group. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Embedded Feishu credentials can expose tenant access if the artifact is shared or installed without review. <br>
Mitigation: Remove and rotate the embedded secret, then require credentials from secure environment configuration before use. <br>
Risk: The skill can update Feishu records and post lead data to a fixed group without clear user confirmation. <br>
Mitigation: Verify the exact Feishu table and group recipients, restrict the Feishu app to least-privilege scopes, and add a dry-run or explicit confirmation step before writing records or sending reports. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/clonbrowser/lead-processor) <br>
- [Publisher Profile](https://clawhub.ai/user/clonbrowser) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, configuration] <br>
**Output Format:** [Structured lead classifications, Feishu table updates, and Feishu text notifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include A/B/C ratings, company type, recommended action, evidence summary, contact clues, risk or exclusion reason, processing status, and update date.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
