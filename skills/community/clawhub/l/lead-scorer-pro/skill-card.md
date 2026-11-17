## Description:

Scores website leads from website audit signals using a weighted rubric, assigns Hot/Warm/Lukewarm/Cold priority tiers, and writes the results to Google Sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:


## Use Case:

Sales, marketing, and lead generation teams use this skill after website auditing and contact enrichment to prioritize website leads and export scored prospects to Google Sheets for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: New Google Sheets may be created with public writer access.

Mitigation: Keep sheets private or share only with specific trusted accounts, and remove any public anyone writer shares.

Risk: Untrusted lead data can be interpreted as formulas when written to Google Sheets.

Mitigation: Write lead values as RAW or sanitize formula prefixes before appending rows.

Risk: Service-account credential files can expose Google Sheets and Drive access if stored in shared locations.

Mitigation: Keep credential files outside shared folders and prefer narrower Google Drive permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maverick-software/skills/lead-scorer-pro)

## Skill Output:

**Output Type(s):** [text, code, configuration]

**Output Format:** [Markdown guidance with Python code snippets and Google Sheets row data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Google Sheets credentials and can append scored lead rows with tier labels and score breakdowns.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
