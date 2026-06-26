## Description: <br>
Searches, briefs, and monitors Naver News in Korean using the Naver Search API, with saved watch rules, keyword groups, and cron-friendly automation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twbeatles](https://clawhub.ai/user/twbeatles) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Korean-speaking operators, analysts, and developers use this skill to turn natural-language Naver News requests into one-shot briefings, saved watch rules, grouped recurring briefings, and scheduler-ready command guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Naver Search API credentials and local monitoring state in its data directory. <br>
Mitigation: Install only where local credential and query storage is acceptable, and use the documented credential setup and check commands before operational use. <br>
Risk: Generated cron and OpenClaw command text can create recurring news checks or forward results to external channels. <br>
Mitigation: Review generated schedule, command, and delivery text before enabling automated runs or message forwarding. <br>
Risk: Briefings are based on Naver Search API headline and summary metadata rather than full article bodies. <br>
Mitigation: Treat briefing output as a search-based digest and open linked sources before using it for consequential decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twbeatles/naver-news-briefing) <br>
- [Naver Search News API endpoint](https://openapi.naver.com/v1/search/news.json) <br>
- [Upstream notes](references/upstream-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Korean text or JSON, with markdown-style command examples for setup and scheduling guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Naver News links, publisher names, publication dates, saved watch or group metadata, cron examples, and OpenClaw systemEvent text.] <br>

## Skill Version(s): <br>
2026.4.16 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
