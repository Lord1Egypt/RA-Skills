## Description:

Searches, briefs, and monitors Korean Naver News through the Naver Search API, including natural-language Korean query cleanup, saved watch rules, keyword groups, multi-query briefings, and cron-friendly automation plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twbeatles](https://clawhub.ai/user/twbeatles)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn Korean news requests into Naver News searches, briefings, persistent watch rules, keyword groups, and operator-ready scheduling guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automation, cron, shell, or OpenClaw task text can include unsafe user-provided request content.

Mitigation: Review generated integration plans and commands before use, especially when the original request came from someone else.

Risk: API secrets may be stored locally in plaintext outside Windows.

Mitigation: Prefer interactive credential setup over command-line secrets, keep data/config.json out of repositories and shared folders, and verify local file permissions.

Risk: Watch state and dedupe history are stored locally.

Mitigation: Keep data/watch_state.db out of repositories and shared folders when using persistent monitoring.

## Reference(s):

- [Skill README](README.md)
- [Upstream notes: navernews-tabsearch](references/upstream-notes.md)
- [ClawHub skill page](https://clawhub.ai/twbeatles/skills/naver-news-briefing)
- [Naver News Search API endpoint](https://openapi.naver.com/v1/search/news.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text or JSON, with shell and cron command snippets in operator guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Naver Search API credentials and uses Naver headline, summary, link, publisher, and timestamp metadata rather than full article bodies.]

## Skill Version(s):

2026.4.16 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
