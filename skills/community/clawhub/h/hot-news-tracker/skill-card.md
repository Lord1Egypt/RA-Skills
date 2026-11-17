## Description:

Tracks Toutiao hot-news rankings and searches news by keyword through the gnomic CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huyi9531](https://clawhub.ai/user/huyi9531)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve the current Toutiao hot list or search recent news for a topic, then summarize ranked items, sources, timestamps, and links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to run user-provided search terms through shell-style commands.

Mitigation: Quote or pass search terms as structured command arguments and avoid executing suspicious input.

Risk: The skill recommends globally installing an unpinned npm CLI if gnomic is unavailable.

Mitigation: Use a pinned, locally reviewed gnomic-cli installation in an environment with limited filesystem and network privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huyi9531/skills/hot-news-tracker)
- [gnomic-cli source](https://github.com/huyi9531/gnomic_cli)
- [Toutiao](https://www.toutiao.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or text summaries with inline shell commands and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ranked hot-list entries, keyword search results, media names, timestamps, summaries, heat values, and URLs.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
