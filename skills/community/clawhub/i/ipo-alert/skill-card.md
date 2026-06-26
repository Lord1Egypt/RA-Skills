## Description: <br>
한국 공모주 청약/신규상장 일정 알림. 38.co.kr에서 데이터 수집, D-1/당일 알림, 주간 요약 제공. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[garibong-labs](https://clawhub.ai/user/garibong-labs) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to monitor Korean IPO subscription and new-listing schedules, receive D-1 and day-of alerts, and generate a weekly summary from public 38.co.kr schedule pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled execution can create recurring requests to 38.co.kr. <br>
Mitigation: Review cron or HEARTBEAT schedules and run the skill only as often as intended. <br>
Risk: The skill writes a local notification state file under the user's home directory. <br>
Mitigation: Install only if local state at ~/.config/ipo-alert/state.json is acceptable for the environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/garibong-labs/ipo-alert) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/garibong-labs) <br>
- [38.co.kr IPO subscription schedule](https://www.38.co.kr/html/fund/index.htm?o=k) <br>
- [38.co.kr new listing schedule](https://www.38.co.kr/html/fund/index.htm?o=nw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown notifications and summaries with optional shell command/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses python3 and curl, requests public 38.co.kr schedule pages, and stores notification state at ~/.config/ipo-alert/state.json.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
