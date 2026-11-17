## Description:

Converts Markdown articles for WeChat Official Accounts, Zhihu, and Toutiao, with draft publishing, code formatting, AI writing, humanization, and cover image generation support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuesf](https://clawhub.ai/user/yuesf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to prepare Markdown articles, generate or revise article content, and create drafts on supported publishing platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing credentials, cookies, and AI API keys are required for normal operation and could expose accounts if mishandled.

Mitigation: Use dedicated or low-privilege publishing accounts where possible, restrict access to configuration files and environment variables, and avoid pasting browser cookies into shared shells.

Risk: Article content, prompts, and media may be sent to external publishing, AI, image generation, or conversion services.

Mitigation: Review every draft or publish command before execution and avoid processing private or proprietary drafts unless the configured service use is approved.

Risk: Cover image paths or URLs can cause local files or remote resources to be uploaded or downloaded.

Mitigation: Pass only trusted cover paths or URLs and inspect referenced files before publishing or generating drafts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuesf/skills/multi-writing-skills)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)
- [Package metadata](artifact/pyproject.toml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown, HTML, shell command snippets, configuration values, generated text, image URLs, and local output files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create platform drafts and send article content, prompts, credentials, and media to configured external services.]

## Skill Version(s):

1.1.3 (source: server release metadata; artifact pyproject.toml reports 1.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
