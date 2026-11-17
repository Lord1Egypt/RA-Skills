## Description:

LLM-maintained knowledge wiki for Obsidian vaults that routes ingest, query, and health workflows for a persistent _wiki knowledge layer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webkong](https://clawhub.ai/user/webkong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain an Obsidian-backed knowledge wiki: ingest durable insights, query synthesized wiki pages, and audit wiki health over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read relevant vault notes and persist model-generated changes under _wiki/.

Mitigation: Install it only in vaults where this access is acceptable, keep version control or backups, and review generated wiki edits.

Risk: Untrusted URLs or sensitive notes may be summarized into persistent wiki content.

Mitigation: Avoid ingesting sources that should not be retained, and inspect synthesized pages before relying on or sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/webkong/skills/llm-wiki-skill)
- [Project homepage](https://github.com/webkong/LLM-Skill)
- [LLM Wiki concept](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Wiki Page Format](skills/llmwiki-ingest/references/wiki-page-format.md)
- [Frontmatter Schema](skills/llmwiki-ingest/references/frontmatter-schema.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown wiki pages, Markdown reports, and concise text answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read vault notes, synthesize content into _wiki/, and update wiki logs when the user invokes ingest, query, or health workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter, CHANGELOG, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
