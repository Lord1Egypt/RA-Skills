## Description: <br>
Scan your GOG library for installed games not played in 30+ days, email the list, and add Apple Reminders for each. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to audit installed GOG games, identify titles that have not been played recently, send a summary email, and create Apple Reminders for cleanup decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script reads local email configuration before sending an HTML report. <br>
Mitigation: Review scripts/sweep.sh before installing, run it with --dry-run first, and confirm the selected himalaya account and recipient address. <br>
Risk: The emailed report can include local game install paths. <br>
Mitigation: Send reports only to an intended recipient and avoid sharing generated email content when install paths are sensitive. <br>
Risk: Cron usage can create recurring automated emails and reminders. <br>
Mitigation: Enable the cron example only when recurring monthly reports are desired, and confirm the Reminders list before scheduling. <br>


## Reference(s): <br>
- [GOG library schema](references/gog_library_schema.json) <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/gog-stale-games-cleanup) <br>
- [JSON Schema draft 2020-12](https://json-schema.org/draft/2020-12/schema) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and script-generated text, HTML email, and Apple Reminders entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq, himalaya, remindctl, a GOG library JSON file, and local email and Apple Reminders configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
