## Description: <br>
Let your agent write notes anywhere: local markdown, Apple Notes, Bear, Obsidian, Notion, Evernote, configurable per note type. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individuals and teams use this skill to have an agent capture, format, route, search, and track notes across local markdown and optional external note platforms. It is suited to meetings, decisions, brainstorms, journals, project updates, quick notes, and action-item follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive note content may be routed to external services when remote platforms are configured. <br>
Mitigation: Keep routing local for sensitive content and require user review before remote writes. <br>
Risk: API tokens or local credential files may be exposed if handled casually. <br>
Mitigation: Store tokens with restrictive permissions and ask for explicit permission before checking credential files. <br>
Risk: Delete or modification commands in connected note tools can affect user notes. <br>
Mitigation: Require review before delete commands or destructive remote writes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/notes) <br>
- [Publisher Profile](https://clawhub.ai/user/ivangdavila) <br>
- [Skill Homepage](https://clawic.com/skills/notes) <br>
- [Notion Integrations](https://notion.so/my-integrations) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes, action tables, configuration guidance, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local markdown files under ~/notes/ and may call configured note-platform tools or APIs after user setup and consent.] <br>

## Skill Version(s): <br>
1.1.3 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
