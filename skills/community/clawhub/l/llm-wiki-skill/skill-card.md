## Description: <br>
LLM-maintained knowledge wiki for Obsidian vaults: ingest sources into a structured _wiki layer, query and synthesize answers, and audit wiki health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[webkong](https://clawhub.ai/user/webkong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to maintain an Obsidian-based personal or project knowledge wiki. It routes requests to ingest sources, answer questions from accumulated wiki pages, and audit the wiki for broken links, stale pages, missing frontmatter, and other quality issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and updates a local Obsidian _wiki/ layer, so generated summaries or edits may persist in the user's vault. <br>
Mitigation: Use backups or version control, review changes after query and health operations, and run it only on notes the user is comfortable summarizing into local wiki pages. <br>
Risk: The health workflow can auto-fix missing frontmatter and orphan pages, which may introduce links or metadata that need human judgment. <br>
Mitigation: Review generated health reports and diffs before relying on the updated wiki for navigation or downstream work. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/webkong/llm-wiki-skill) <br>
- [Project Homepage](https://github.com/webkong/LLM-Skill) <br>
- [Wiki Page Format](skills/llmwiki-ingest/references/wiki-page-format.md) <br>
- [Frontmatter Schema](skills/llmwiki-ingest/references/frontmatter-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Markdown reports, synthesized answers, and structured wiki page updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read vault notes, update _wiki/ pages, append to _wiki/log.md, and report gaps or issues needing human review.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
