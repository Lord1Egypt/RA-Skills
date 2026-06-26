## Description: <br>
A daily lyrics blessing skill that sends a random Hetu song lyric and blessing message to a designated recipient, with lyrics fetched from Baidu Baike using agent-browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Trae1ounG](https://clawhub.ai/user/Trae1ounG) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to send scheduled daily reminder or warm-message emails that include verified Hetu lyrics and a blessing message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hardcoded SMTP credentials and a fixed recipient could cause email to be sent through someone else's account if the skill is run as-is. <br>
Mitigation: Remove hardcoded credentials and recipient values, rotate the exposed credential if it is yours, and use user-controlled secure configuration before any execution. <br>
Risk: Scheduling the script with cron could repeatedly send unwanted reminder emails. <br>
Mitigation: Preview the outgoing email manually first and only add the cron job after confirming how to disable or remove the schedule. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Trae1ounG/hetu-lyrics-blessing) <br>
- [Baidu Baike](https://baike.baidu.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and plain text email output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-controlled SMTP configuration and review before scheduling automated sends.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
