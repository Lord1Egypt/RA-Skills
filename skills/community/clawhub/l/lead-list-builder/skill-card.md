## Description: <br>
Operates as an autonomous lead-list building agent that discovers businesses with outdated or broken websites, audits each site, enriches contact information, scores leads, and writes results to a Google Sheet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales teams, agencies, and developers use this skill to build local business prospect lists by niche and region. It coordinates search, website auditing, contact enrichment, lead scoring, and Google Sheets delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys and Google service account credentials could grant access beyond this workflow. <br>
Mitigation: Use dedicated low-privilege keys, share only the intended sheet with the service account, and keep .env and credentials.json out of source control. <br>
Risk: The workflow collects and stores business contact details for outreach. <br>
Mitigation: Limit sheet access to intended users, review collected data before use, and follow applicable privacy and outreach rules. <br>
Risk: The workflow may query third-party search and enrichment services. <br>
Mitigation: Review which services are configured, understand what data is sent to them, and monitor quota and terms-of-service constraints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maverick-software/lead-list-builder) <br>
- [Lead List Builder Setup Guide](references/setup-guide.md) <br>
- [Search Query Library](references/query-library.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status summaries, setup guidance, command examples, and Google Sheets lead rows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write collected lead data to a user-configured Google Sheet and relies on user-provided API credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
