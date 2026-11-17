## Description:

한국 공모주 청약/신규상장 일정 알림. 38.co.kr에서 데이터 수집, D-1/당일 알림, 주간 요약 제공.

This skill is ready for commercial/non-commercial use.

## Publisher:

[garibong-labs](https://clawhub.ai/user/garibong-labs)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to monitor Korean IPO subscription and new-listing schedules from 38.co.kr, generate D-1 and day-of alerts, and produce weekly summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alert content depends on data fetched from 38.co.kr and may become stale or reflect upstream website changes.

Mitigation: Review generated alerts before acting on them and confirm important IPO dates against authoritative sources.

Risk: Cron or HEARTBEAT automation can run the script repeatedly and store notification history in ~/.config/ipo-alert/state.json.

Mitigation: Review any scheduled automation before enabling it and clear the state file when resetting notification history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/garibong-labs/skills/ipo-alert)
- [38.co.kr IPO subscription schedule](https://www.38.co.kr/html/fund/index.htm?o=k)
- [38.co.kr new listing schedule](https://www.38.co.kr/html/fund/index.htm?o=nw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown-style Korean alert text with inline links and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches fixed 38.co.kr schedule pages and keeps notification history in ~/.config/ipo-alert/state.json to reduce duplicate alerts.]

## Skill Version(s):

0.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
