## Description: <br>
Chat-native Customer Relationship Management system designed for one-person agencies, freelancers, and small Belgian businesses managing multiple client relationships and complex sales pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexaiguy](https://clawhub.ai/user/nexaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and small-business operators use this skill to manage prospects, sales pipeline stages, activity history, follow-up reminders, and CRM exports through an agent-operated local CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prospect, contact, notes, interaction history, and deal data are stored locally and may include sensitive business information. <br>
Mitigation: Install only when local storage under ~/.nex-crm is acceptable, restrict filesystem access to that directory, and back it up according to the user's data policy. <br>
Risk: CSV or JSON exports can expose customer and deal data if placed in shared or synced folders. <br>
Mitigation: Treat exports as sensitive files and confirm the destination and intent before generating or sharing them. <br>
Risk: Ambiguous agent requests could create, update, or export CRM records unexpectedly. <br>
Mitigation: Ask the user to confirm before write, stage-change, reminder, or export operations when the request is unclear. <br>


## Reference(s): <br>
- [Nex CRM README](README.md) <br>
- [Nex AI homepage](https://nex-ai.be) <br>
- [ClawHub skill page](https://clawhub.ai/nexaiguy/nex-crm) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, CSV, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text summaries, optional JSON command output, CSV or JSON exports, and shell commands for local CRM operations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate on local SQLite data under ~/.nex-crm and may create export files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
