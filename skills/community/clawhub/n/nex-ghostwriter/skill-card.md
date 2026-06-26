## Description: <br>
Nex Ghostwriter helps an agent turn meeting notes into client follow-up emails or internal recaps, track drafts and contacts, search meeting history, view statistics, and export locally stored meeting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexaiguy](https://clawhub.ai/user/nexaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, consultants, freelancers, sales teams, account managers, project managers, and founders use this skill to draft meeting follow-up emails and internal recaps from notes, action items, next steps, and contact details. It also helps agents manage local meeting records, draft status, contact greetings, search, statistics, and CSV or JSON exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting notes, client emails, contacts, action items, and generated drafts are retained locally. <br>
Mitigation: Only log information you are comfortable storing under ~/.nex-ghostwriter/, and avoid regulated secrets unless local retention practices allow them. <br>
Risk: Generated follow-up drafts may omit nuance or reflect incomplete meeting notes. <br>
Mitigation: Review each draft before sending, especially action owners, deadlines, commitments, client names, and tone. <br>
Risk: CSV or JSON exports can expose accumulated meeting history outside the local database. <br>
Mitigation: Export only when needed and handle exported files according to the sensitivity of the underlying meeting records. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nexaiguy/nex-ghostwriter) <br>
- [Nex AI homepage](https://nex-ai.be) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown-style email or recap drafts, with CLI command guidance and CSV or JSON export files when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores meeting notes, contacts, drafts, and exports locally under ~/.nex-ghostwriter/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
