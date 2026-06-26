## Description: <br>
Manage and navigate a multi-layered, branch-based memory system that organizes agent context into Root, Domain, and Project layers and can create local markdown files for memory branches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[balkanblbn](https://clawhub.ai/user/balkanblbn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to structure long-term workspace memory so an agent can recall relevant context without loading every memory file. It supports creating and linking Root, Domain, and Project memory branches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script can modify persistent workspace files and may update unintended memory files if unsafe branch names or parent paths are supplied. <br>
Mitigation: Use simple slug-like branch names, pass only intended memory or domain markdown files as parents, and review file changes before relying on the updated memory map. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/balkanblbn/hierarchical-memory) <br>
- [Publisher profile](https://clawhub.ai/user/balkanblbn) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and local markdown memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update persistent workspace memory files when the helper script is run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
