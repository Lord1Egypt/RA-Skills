## Description:

This skill helps OpenClaw agents ingest documents, compile them into an LLM-maintained Markdown knowledge wiki, query the knowledge base, and sync entries with Obsidian.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to turn URLs, files, text snippets, WeChat articles, and GitHub content into an auditable Markdown knowledge base with indexes, links, logs, graph views, Obsidian sync, and synthesized answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently write knowledge-base files and bootstrap-generated workspace instruction files.

Mitigation: Review before installing, use a dedicated KB directory and vault subfolder, and back up active workspaces before running bootstrap-from-questionnaire.sh.

Risk: Compiled documents and questions may be sent to the configured LLM provider.

Mitigation: Avoid sensitive documents unless prompt content may be shared with that provider, and review the local model/provider configuration before use.

Risk: The security evidence identifies filename validation and questionnaire parsing issues for untrusted inputs.

Mitigation: Do not use the skill with untrusted content or filenames until those issues are fixed; sanitize inputs and review generated files before relying on them.

## Reference(s):

- [Karpathy LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [LLM Wiki v2 gist](https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2)
- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-openclaw-openai-knowledge-base)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal text, Markdown wiki files, shell command guidance, JSON configuration, Obsidian base files, and Mermaid graph files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append logs, indexes, generated wiki entries, Obsidian-synced files, and saved answers within the configured agent or shared knowledge-base scope.]

## Skill Version(s):

2.8.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
