## Description: <br>
Manage Microsoft 365 email, calendar, and contacts through the ms365 CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thecfguy](https://clawhub.ai/user/thecfguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and their agents use this skill to inspect and manage Microsoft 365 email, calendar, and contacts from a terminal-backed workflow. It supports reading and searching account data plus account-changing actions such as sending mail, moving or deleting messages, creating folders, and creating or deleting calendar events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent live Microsoft 365 account-changing powers, including sending email, moving or deleting messages, creating folders, and changing calendar events. <br>
Mitigation: Use the narrowest delegated Microsoft 365 permissions available and require the agent to show the exact item and command before any send, move, delete, folder, or calendar change. <br>
Risk: Authentication and tokens are handled by the local ms365 CLI for a real user account. <br>
Mitigation: Have the user authenticate manually only when needed, check auth status before use, and run ms365 auth logout when finished. <br>
Risk: Incorrect IDs, broad queries, or permanent deletion can expose or remove more mailbox or calendar data than intended. <br>
Mitigation: Verify item IDs from list or search results, keep result counts bounded, and avoid permanent deletion unless the user explicitly requests it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thecfguy/ms365-cli) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bounded CLI queries by default and requires user-authenticated Microsoft 365 access before account operations can run.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
