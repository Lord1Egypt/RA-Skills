## Description:

Obsidian Librarian helps an agent save URLs, articles, social posts, pasted text, or local text files into an Obsidian vault as categorized, wikilinked markdown notes and answer questions over the saved vault with RAG.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shahalay007](https://clawhub.ai/user/shahalay007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to capture research material into an Obsidian knowledge base, organize it as markdown with frontmatter and wikilinks, and query saved notes with cited answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private vault notes, pasted files, URLs, or retrieved web content may be sent to external services used by the skill.

Mitigation: Use the skill only with vaults, files, and URLs that are acceptable to process through Gemini, Apify, Brave search fallback, and optional Supabase services.

Risk: Path-scope flaws may allow files outside the intended vault inbox to be read or deleted.

Mitigation: Constrain or patch inbox-file and symlink handling before using the skill with sensitive files, and keep inbox files until deletion behavior is reviewed.

Risk: Supabase-backed vector storage can expose vault content if the endpoint or schema access controls are not trustworthy.

Mitigation: Enable Supabase only with a trusted HTTPS endpoint and per-user access controls applied to the configured schema.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shahalay007/skills/obsidian-librarian)
- [Project homepage](https://github.com/openclaw/obsidian-librarian)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown notes, JSON RAG output, and agent-facing text with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write categorized Obsidian notes with YAML frontmatter, maintain a local JSON or Supabase-backed vector index, and return cited answers from vault content.]

## Skill Version(s):

0.2.7 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
