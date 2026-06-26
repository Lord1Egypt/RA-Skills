## Description: <br>
Manages Microsoft 365 junk mail by analyzing Outlook/Exchange spam patterns, assigning suspicious scores, and helping review or move messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tradmangh](https://clawhub.ai/user/tradmangh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, mailbox administrators, and support operators use this skill to inspect Microsoft 365 junk folders, score suspected spam, and move selected messages to the inbox or a learning folder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify Microsoft 365 mailbox contents, including moving messages. <br>
Mitigation: Install only where mailbox read/write access is acceptable, run analysis first, and verify the target mailbox and message IDs before running move commands. <br>
Risk: Security evidence reports that mailbox-management scripts can modify email without the confirmations promised in documentation. <br>
Mitigation: Use --dryRun true for check-spam.mjs, prefer review workflows, and manually confirm any mailbox-changing action before relying on the result. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require Microsoft 365 profile configuration and mailbox read/write permissions before mailbox-changing commands can run.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
