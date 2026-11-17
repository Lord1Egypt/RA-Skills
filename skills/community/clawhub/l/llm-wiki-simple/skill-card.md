## Description:

LLM Wiki Simple helps an agent scan user-provided source documents and rewrite them into a structured personal Markdown wiki.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwl52](https://clawhub.ai/user/wwl52)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to turn articles, notes, papers, and code snippets into categorized Obsidian-style wiki pages. It supports building and refreshing a local personal knowledge base from files the user intentionally places in a raw input folder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive or private documents placed in 00_Raw/ may be summarized into generated wiki pages.

Mitigation: Only place documents in 00_Raw/ that are appropriate for agent and model processing, and review generated pages before sharing them.

Risk: Generated or refreshed pages in 01_Wiki/ can overwrite same-named wiki content, including manual edits outside preserved sections.

Mitigation: Review generated or overwritten pages, and keep important manual notes under version control or outside generated sections.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwl52/skills/llm-wiki-simple)
- [Obsidian](https://obsidian.md/)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown files and concise text status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates a local Raw/Wiki/System folder structure and may overwrite same-named generated wiki pages.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
