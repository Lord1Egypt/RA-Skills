## Description: <br>
Generate and deliver a Hacker News daily report with Top-N article summaries and multi-view comment synthesis in a user-selected language, with optional file persistence and index updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liu7yong](https://clawhub.ai/user/liu7yong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent fetch current Hacker News stories, gather article snippets and comments, and produce a concise daily Markdown brief. It can also persist the report and maintain an index when configured to do so. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches live Hacker News content and linked article pages, so generated briefs may reflect unavailable, incomplete, or changing source material. <br>
Mitigation: Review the generated brief before relying on it, and keep the source/comment separation and short-source markers required by the skill enabled. <br>
Risk: When persistence or scheduling is enabled, the agent can write report files locally and create recurring runs. <br>
Mitigation: Review outputDir, persist, and reminderTime before enabling scheduled operation, and use the built-in retry and idempotency checks to avoid duplicate reports. <br>


## Reference(s): <br>
- [Hacker News Firebase API](https://hacker-news.firebaseio.com/v0) <br>
- [HN Daily Brief on ClawHub](https://clawhub.ai/liu7yong/hn-daily-brief) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Files, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown report delivered in chat, optional Markdown files and index updates, and intermediate JSON materials for report generation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Configurable language, Top-N count, strict or lite style, output directory, persistence, and optional scheduled reminder time.] <br>

## Skill Version(s): <br>
0.8.2 (source: server release evidence and release notes) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
