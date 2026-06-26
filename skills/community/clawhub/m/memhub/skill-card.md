## Description: <br>
MemHub lets agents read, write, search, archive, export, and sync a user's cross-agent memory repository using MemHub Protocol v0.1. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cutd](https://clawhub.ai/user/cutd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to give compatible agents durable personal or project memory, retrieve context at session start, record stable facts, preferences, and decisions, export chatbot context, and sync memory through GitHub or Gitee. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to store durable personal and project memory. <br>
Mitigation: Review what the agent writes, use inbox review for low-confidence content, and avoid saving secrets or sensitive personal data. <br>
Risk: Remote sync may push memory to GitHub or Gitee, where content can remain in repository history. <br>
Mitigation: Enable sync only for repositories and accounts you trust, prefer private repositories for personal memory, and treat soft-archived entries as retained history rather than deletion. <br>
Risk: OAuth or token-based sync requires credentials and may use the default OAuth broker. <br>
Mitigation: Use token, SSH, or a trusted broker if the default broker is not acceptable, and never paste access tokens, OAuth codes, or client secrets into chat or committed files. <br>


## Reference(s): <br>
- [MemHub Skill README](README.md) <br>
- [MemHub Skill Instructions](SKILL.md) <br>
- [ClawHub MemHub Skill Page](https://clawhub.ai/cutd/skills/memhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text guidance with inline shell commands; the CLI can also write YAML and Markdown files in the configured memory repository.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists user-selected memory locally and can sync it to a user-configured GitHub or Gitee repository.] <br>

## Skill Version(s): <br>
0.4.4 (source: frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
