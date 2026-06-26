## Description: <br>
Helps agents use the Notion API to create, update, and query pages, with workflows for saving ideas and tracking related milestones in configured Notion databases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuyangmiemie-beep](https://clawhub.ai/user/xuyangmiemie-beep) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to connect an agent to Notion, persist idea records, convert ideas into planned work, and create or update milestone entries after reviewing confirmation prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write records to Notion databases after user approval. <br>
Mitigation: Read each confirmation prompt carefully and approve only intended idea or milestone writes. <br>
Risk: A Notion integration token is required for API access. <br>
Mitigation: Use a dedicated least-privilege token and protect the local ~/.config/notion/api_key file. <br>
Risk: The bundled workflows target configured database IDs. <br>
Mitigation: Confirm the database IDs match the intended Notion workspace before using write workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuyangmiemie-beep/notion-ideas-tracker) <br>
- [Notion API documentation](https://developers.notion.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON examples, bash commands, and Python helper script guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled write scripts read JSON from stdin, show a confirmation prompt, and return Notion page links after successful writes.] <br>

## Skill Version(s): <br>
1.1.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
