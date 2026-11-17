## Description:

Omnipublisher converts one Markdown article into platform-specific Markdown versions for WeChat, Xiaohongshu, Zhihu, and Douyin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utopiabenben](https://clawhub.ai/user/utopiabenben)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, content teams, and developers use this skill to reformat a single article into multiple social publishing variants. It supports local conversion into WeChat, Xiaohongshu, Zhihu, and Douyin Markdown outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the user-provided article file, so sensitive article content could be processed locally by the tool.

Mitigation: Run it only on intended input files and avoid using sensitive drafts unless local processing is acceptable.

Risk: Generated Markdown files are written into the selected output directory and may overwrite similarly named outputs.

Mitigation: Use a dedicated output folder and review generated files before sharing or publishing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utopiabenben/skills/omnipublisher)
- [Publisher profile](https://clawhub.ai/user/utopiabenben)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Guidance]

**Output Format:** [Markdown files and plain-text CLI status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.7+ and writes one Markdown file per selected platform into the chosen output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
