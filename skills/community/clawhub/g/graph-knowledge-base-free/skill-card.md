## Description: <br>
Graph Knowledge Base Free helps agents maintain a local, file-based knowledge base by adding entity facts, superseding outdated facts, and generating summaries from active facts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals, teams, and operators can use this skill to keep evolving records for people, projects, learning notes, or configuration changes. It is intended for workflows that need traceable fact history, replacement of outdated facts, and current Markdown summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for local read, write, and shell execution authority without a bundled executable script or a clearly scoped working directory. <br>
Mitigation: Install only if those capabilities are acceptable, choose a specific knowledge-base directory before use, and review proposed commands and file changes before execution. <br>
Risk: The documentation includes delete, import, export, analytics, and visualization wording that may exceed the clearly supported free-version workflow. <br>
Mitigation: Treat those behaviors as unsupported unless the publisher provides corrected documentation and supporting files; rely on the core add, list, supersede, and summarize workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/graph-knowledge-base-free) <br>
- [SkillHub homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-style responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local knowledge-base files such as items.json and summary.md when executed by an agent with write access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
