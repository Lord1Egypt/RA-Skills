## Description: <br>
Junyi Vault Organizer helps agents route, distill, and save business and personal knowledge as structured notes in a configured Obsidian vault. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuanranc](https://clawhub.ai/user/xuanranc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and knowledge workers use this skill to archive articles, notes, class material, family observations, conversations, ideas, reflections, quotes, and reusable methods into a two-domain Obsidian vault structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad save and remember trigger phrases may cause content to be persistently archived unintentionally. <br>
Mitigation: Use explicit archiving requests, avoid vague save phrases around sensitive content, and review proposed writes before allowing them. <br>
Risk: The skill creates and updates real files in an Obsidian vault. <br>
Mitigation: Configure vault_path to the narrow intended vault, keep backups before first use, and confirm the target path before writing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuanranc/junyi-vault-organizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes, JSON manifests, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local text files to a configured vault path when invoked for archiving.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
