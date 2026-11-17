## Description:

Create a cited Chinese or English personal news brief from public RSS/Atom feeds, filter by topic and calendar days, and save a local Markdown report. Use for My Daily Brief, daily AI/technology digests, or practising a first useful OpenClaw Skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an OpenClaw agent to gather dated updates from selected public RSS/Atom feeds, filter them by topic and calendar dates, and produce a concise cited news brief in Chinese or English. The agent saves the brief as a local Markdown report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public feed servers receive the request IP address, and the connected model processes the collected evidence.

Mitigation: Use public feeds and consider the connected model service's privacy and billing terms.

Risk: Feed updates or generated summaries may be delayed or inaccurate.

Mitigation: Check the original source links before relying on a summary.

Risk: Local evidence, drafts, and reports remain in the workspace until removed.

Mitigation: Remove local brief files when they are no longer needed.

## Reference(s):

- [Options, sources and limits](references/options.md)
- [ClawHub release page](https://clawhub.ai/hznetnewpower/skills/mochi-daily-brief)
- [MochiLab](https://mochilab.bz)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)
- [OpenClaw skill format documentation](https://docs.openclaw.ai/clawhub/skill-format)
- [OpenAI News feed](https://openai.com/news/rss.xml)
- [Google AI feed](https://blog.google/technology/ai/rss/)
- [GitHub Changelog feed](https://github.blog/changelog/feed/)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Cited Markdown news brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One report with a selected language, date window, topics, and up to 20 items.]

## Skill Version(s):

1.0.1 (source: metadata.openclaw.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
