## Description: <br>
Especialista em Obsidian com dominio em Zettelkasten, PARA, BASB, MOCs, Dataview, Templater e organizacao estruturada de vaults. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[playandogamer150-commits](https://clawhub.ai/user/playandogamer150-commits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Obsidian power users use this skill to let an agent organize, search, summarize, and maintain a local Obsidian vault through the Local REST API. It supports note CRUD, folders, Canvas, templates, Dataview-style queries, tasks, backlinks, vault health checks, MOCs, and Zettelkasten workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad read, write, delete, move, merge, and command authority over a private Obsidian vault. <br>
Mitigation: Install only for vaults where this level of control is acceptable, start with a test or backed-up vault, and require explicit confirmation for destructive or bulk actions. <br>
Risk: Misconfigured REST API access can expose sensitive vault content or allow unintended local actions. <br>
Mitigation: Keep the Obsidian Local REST API bound to localhost, restrict the API key, and store credentials in local environment variables. <br>
Risk: Automated organization, Dataview queries, and vault health actions can create incorrect structure, links, tags, or summaries. <br>
Mitigation: Review proposed moves, merges, overwrites, generated links, and obsidian-command actions before applying them to a production vault. <br>


## Reference(s): <br>
- [Obsidian Perfect on ClawHub](https://clawhub.ai/playandogamer150-commits/obsidian-master) <br>
- [Publisher profile](https://clawhub.ai/user/playandogamer150-commits) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text responses, JSON-like tool results, and shell snippets for setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Obsidian, the Local REST API plugin, Node.js 18+, OBSIDIAN_API_KEY, and OBSIDIAN_URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
