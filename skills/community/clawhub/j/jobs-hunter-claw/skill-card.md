## Description: <br>
Automates job discovery, application submission, pipeline tracking, and activity logging with Google Sheets as the central data store. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QuantDeveloperUSA](https://clawhub.ai/user/QuantDeveloperUSA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers and their agents use this skill to maintain a job-search pipeline, add and update opportunities, log recruiter or interview activity, and run periodic follow-up reviews through Google Sheets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is flagged as suspicious because it enables broad unattended job-search automation and Google Sheets write access. <br>
Mitigation: Review and patch the job-tracker shell script before use, keep the spreadsheet private, and restrict mail, calendar, and channel scopes before enabling cron automation. <br>
Risk: Untrusted email, recruiter, or job-board text may be ingested into the workflow and written to the tracking sheet. <br>
Mitigation: Define redaction rules and confirm what data may be stored before allowing the agent to process external job-search content. <br>
Risk: Delete and force operations can remove tracker rows while automation is running. <br>
Mitigation: Back up the spreadsheet and require review before using delete or --force operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/QuantDeveloperUSA/jobs-hunter-claw) <br>
- [Google Sheet Setup Guide](references/google-sheet-setup.md) <br>
- [gog CLI](https://gogcli.sh) <br>
- [Google Sheets](https://sheets.google.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Google Sheets-backed job records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gog CLI and a configured JOB_TRACKER_SPREADSHEET_ID environment variable.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence and artifact version history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
