## Description: <br>
Scan your GOG library for installed games not played in 30+ days, email the list, and add reminders to consider uninstalling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to identify installed GOG games that have not been played recently, receive a report, and create reminders before deciding whether to uninstall them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The emailed report may include game names and local install paths. <br>
Mitigation: Run the dry run first and confirm the Himalaya account and intended recipient before a full run. <br>
Risk: A full run creates Apple Reminders entries and repeated scheduled runs may add more reminders. <br>
Mitigation: Use dry-run mode for review and enable any cron schedule only after confirming the reminder list and desired cadence. <br>
Risk: The scan depends on a local GOG library JSON file and configured command-line tools. <br>
Mitigation: Confirm the GOG library path, Himalaya account, and remindctl setup before running outside dry-run mode. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/gog-stale-games) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and formatted terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send an HTML email and create Apple Reminders entries when not run in dry-run mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
