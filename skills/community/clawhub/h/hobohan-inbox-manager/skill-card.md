## Description: <br>
Authorize, read, triage, archive, trash, and summarize Gmail inboxes across multiple accounts. Uses Gmail API with OAuth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hohobohan](https://clawhub.ai/user/hohobohan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Gmail inboxes across multiple accounts, including reading, filtering, triaging, archiving, trashing, and summarizing messages through OAuth-authorized Gmail API access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth client secrets and token files can grant ongoing Gmail account access if exposed. <br>
Mitigation: Keep OAuth files private, never commit token files, and use the skill only with Gmail accounts intended for agent-managed inbox operations. <br>
Risk: Bulk archive or trash operations can affect many messages when the account or Gmail query is too broad. <br>
Mitigation: Require the agent to show the exact account, query, message count, and representative sample messages before archive or trash actions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Gmail OAuth credentials and per-account token files for live mailbox operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and CHANGELOG.md, released 2026-06-03) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
