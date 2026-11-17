## Description:

Reads Obsidian Publish document links and helps an agent retrieve complete article or note content, preferring direct fetches and falling back to browser snapshots when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theopenbase](https://clawhub.ai/user/theopenbase)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need an agent to read user-provided Obsidian Publish articles, notes, and essays and return the extracted text or a summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill retrieves text from user-provided Obsidian Publish links, so the returned content may reflect incomplete fetches or untrusted external content.

Mitigation: Use it with intended Obsidian Publish URLs and review retrieved text before relying on summaries or downstream actions.

Risk: The skill instructions are written in Chinese, which may make review harder for non-Chinese-speaking users.

Mitigation: Have a Chinese-speaking reviewer or a trusted translation confirm the workflow before deployment.

## Reference(s):

- [Obsidian Read ClawHub release](https://clawhub.ai/theopenbase/skills/obsidian-read)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text containing retrieved Obsidian Publish content, extracted text, summaries, or tool-use guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide the agent to try direct fetches first and browser snapshots when direct fetching is incomplete or fails.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
