## Description: <br>
Find GOG games installed but not played for 30+ days, email the list, and add Apple Reminders to consider uninstalling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to identify stale installed GOG games, receive a digest, and create reminders to consider uninstalling them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send email through the configured Himalaya account. <br>
Mitigation: Set EMAIL_TO explicitly before a full run, or run with SKIP_EMAIL=1 when email output is not desired. <br>
Risk: The skill can create Apple Reminders entries. <br>
Mitigation: Run with SKIP_REMINDERS=1 when reminder creation is not desired, and review the target reminders list before recurring use. <br>
Risk: A recurring cron schedule can repeatedly send reports or create reminders. <br>
Mitigation: Review any cron schedule before enabling recurring reports. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/gog-cleanup) <br>
- [Publisher Profile](https://clawhub.ai/user/terrycarter1985) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; runtime outputs include console text, HTML email, and Apple Reminders entries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses jq, himalaya, and remindctl; SKIP_EMAIL, SKIP_REMINDERS, STALE_DAYS, EMAIL_TO, and REMINDERS_LIST adjust runtime behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
