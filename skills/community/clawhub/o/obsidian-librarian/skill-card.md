## Description: <br>
Obsidian Librarian saves URLs, articles, social posts, pasted text, and local files into an Obsidian vault as categorized, wikilinked Markdown notes, then answers questions over the vault with RAG. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shahalay007](https://clawhub.ai/user/shahalay007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to capture research material into an Obsidian vault, organize it as Markdown notes, and query saved notes with grounded answers and citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can index and send private, regulated, client, or proprietary vault content to external AI services. <br>
Mitigation: Use a dedicated vault or tightly scoped OBSIDIAN_VAULT_PATH, and review vault contents before enabling the skill on sensitive material. <br>
Risk: Supabase-backed search stores searchable chunks outside the local vault when Supabase settings are enabled. <br>
Mitigation: Leave Supabase disabled unless external vector storage is acceptable, and confirm the target database and retention policy before use. <br>
Risk: Broad save prompts may preserve sensitive conversations or unintended context as notes. <br>
Mitigation: Use explicit save requests and inspect staged content before saving conversations that may contain sensitive information. <br>
Risk: Shortened or linked URLs may be resolved from the local runtime before ingestion. <br>
Mitigation: Avoid ingesting untrusted shortened URLs, or expand and inspect them before asking the skill to save them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shahalay007/obsidian-librarian) <br>
- [Project homepage](https://github.com/openclaw/obsidian-librarian) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, configuration] <br>
**Output Format:** [Markdown notes, JSON search results, and concise text answers with source citations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write note files and local or Supabase-backed vector indexes for vault search.] <br>

## Skill Version(s): <br>
0.2.7 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
