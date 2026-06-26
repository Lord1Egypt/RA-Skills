## Description: <br>
帮助代理构建、维护、查询、归档和体检由 LLM 持续维护的 Markdown/Obsidian 知识 Wiki。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengsusky](https://clawhub.ai/user/fengsusky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to initialize and maintain a Markdown/Obsidian knowledge vault, import source materials, update wiki pages, answer from the wiki, archive durable answers, and audit link, index, coverage, and encoding health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk import, rename, or restructuring work can misplace notes, break wikilinks, or alter user-maintained organization. <br>
Mitigation: Back up important notes, review proposed move or rename mappings before execution, and run the packaged audit script after changes. <br>
Risk: Markdown wiki edits can introduce broken links, missing index entries, source coverage gaps, or UTF-8 encoding issues. <br>
Mitigation: Use scripts/verify_wiki.py to check source coverage, broken wikilinks, index coverage, and UTF-8 issues, then manually review reported issues. <br>
Risk: Optional web-sourced additions may mix unverified current information into stable knowledge pages. <br>
Mitigation: Prefer official sources, papers, and original announcements, label externally verified facts, and keep them distinct from source-text claims. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fengsusky/llm-wiki-cn) <br>
- [Publisher profile](https://clawhub.ai/user/fengsusky) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Wiki audit script](artifact/scripts/verify_wiki.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, wikilinked file edits, structured check results, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and edits user-selected vault content; includes a local read-only audit script for coverage, broken links, index coverage, and UTF-8 checks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
