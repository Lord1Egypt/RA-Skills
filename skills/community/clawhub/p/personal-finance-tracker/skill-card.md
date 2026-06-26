## Description: <br>
Track personal finances with cashflow reviews, recurring bill detection, debt triage, CSV imports, and net worth snapshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to analyze personal cashflow, recurring bills, debt pressure, transaction CSVs, and short-term runway so they can make clearer budgeting and payment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process sensitive pasted transactions or finance CSVs. <br>
Mitigation: Use it only when the user is comfortable sharing that data with the agent, and keep analysis local when possible. <br>
Risk: Optional local continuity files may retain financial context beyond a single session. <br>
Mitigation: Create or update the local memory folder only with user consent, avoid credentials and full statements, and periodically review or delete saved notes. <br>
Risk: Budgeting or debt guidance can be mistaken for regulated financial advice or account control. <br>
Mitigation: Keep recommendations transparent, reversible, grounded in user-provided data, and do not move money, cancel services, or access accounts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/personal-finance-tracker) <br>
- [Personal Finance Tracker Homepage](https://clawic.com/skills/personal-finance-tracker) <br>
- [Setup](artifact/setup.md) <br>
- [CSV Schema](artifact/csv-schema.md) <br>
- [Commands](artifact/commands.md) <br>
- [Debt Triage](artifact/debt-triage.md) <br>
- [Review Rhythm](artifact/review-rhythm.md) <br>
- [Memory Template](artifact/memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with optional shell commands, Python script outputs, and local configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize user-provided financial data and optional local files only with user consent.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
