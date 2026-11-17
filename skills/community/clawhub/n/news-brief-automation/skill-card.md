## Description:

Build, refine, or maintain recurring news-digest workflows that periodically collect items from sources such as Hacker News, GitHub Trending, Hugging Face, RSS feeds, blogs, and specific news sites; deduplicate against the newest prior report; save a Markdown brief in the workspace; and send the same summary to the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[louishwh](https://clawhub.ai/user/louishwh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create reusable scheduled news-digest prompts, stable Markdown report formats, and deduplication rules for daily, weekly, or intraday briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: News briefs can become misleading if source lists, schedules, selection criteria, or output language are not confirmed before recurring use.

Mitigation: Confirm the sources, cadence, criteria, report folder, and delivery expectations before enabling the automation.

Risk: Recurring runs write prompt and report files into the workspace.

Mitigation: Review the automation/cron/ prompt path and reports/ save path before deployment, and keep the save-first behavior so deduplication has a stable baseline.

## Reference(s):

- [Examples](artifact/references/examples.md)
- [Templates](artifact/references/templates.md)
- [Hacker News](https://news.ycombinator.com/)
- [Hacker News Newest](https://news.ycombinator.com/newest)

## Skill Output:

**Output Type(s):** [Markdown, Files, Configuration, Guidance]

**Output Format:** [Markdown instructions and reusable prompt templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create workspace prompt files under automation/cron/ and Markdown reports under reports/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
