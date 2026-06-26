## Description: <br>
Scan installed GOG games, find titles inactive for 30+ days, email the list to the configured personal address, and add Apple Reminders in the Gaming list for uninstall review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and personal automation users use this skill to review installed GOG games that have not been played recently, preview the cleanup list, and optionally send themselves an email summary and Apple Reminders for uninstall review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A real run can send one email and create one Apple Reminder for each stale installed game found. <br>
Mitigation: Run the documented dry-run first, then verify config/gog_library.json and config/himalaya.toml point to the intended game library and personal email account before a real run. <br>


## Reference(s): <br>
- [Sample cron schedule](references/sample-cron.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, JSON] <br>
**Output Format:** [Markdown guidance with bash examples; runtime output is plain text with optional JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run mode previews the email body and JSON payload without sending email or creating reminders.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
