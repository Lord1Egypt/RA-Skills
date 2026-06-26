## Description: <br>
Clean and organize Gmail accounts in bulk. Use when asked to clean Gmail, remove spam, trash newsletters/promotional emails, bulk-delete emails by sender, create labels, set up auto-filters, or restore emails from trash. Handles single or multiple Gmail accounts via OAuth token files. Works with any Gmail account using the Gmail API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cedarscy](https://clawhub.ai/user/cedarscy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to scan Gmail accounts, bulk clean messages, organize labels and filters, and restore messages from Trash through Gmail API scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can permanently delete Gmail messages, including Trash purging in deep_clean.py and explicit permanent deletion in clean.py. <br>
Mitigation: Run scan.py and dry-run modes first, prefer moving messages to Trash, and use --skip-trash-purge unless permanent removal is intended. <br>
Risk: The skill can create persistent Gmail labels and filters that affect future messages. <br>
Mitigation: Review label and filter configuration before running organize.py, and use --skip-filters when persistent filter creation is not required. <br>
Risk: Reusable Gmail OAuth tokens are stored as .pkl files on disk. <br>
Mitigation: Store token files in a protected location, restrict local file access, and revoke tokens when access is no longer needed. <br>
Risk: The scripts may install Python dependencies at runtime. <br>
Mitigation: Install dependencies yourself in a trusted environment before running the scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cedarscy/gmail-cleaner) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/cedarscy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides an agent to run local Python scripts that call the Gmail API and may modify mailbox state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
