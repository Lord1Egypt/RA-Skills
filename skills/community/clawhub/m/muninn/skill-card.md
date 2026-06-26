## Description: <br>
Muninn is a per-project memory MCP server that provides local project indexing, semantic context search, and persistent memories for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[endgegnerbert-tech](https://clawhub.ai/user/endgegnerbert-tech) <br>

### License/Terms of Use: <br>
UNLICENSED <br>


## Use Case: <br>
Developers and agent users use Muninn to initialize local project memory, orient an agent with project context, search indexed context, and persist decisions or preferences as Markdown memories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite agent instruction files and enforce future agent behavior without clear approval. <br>
Mitigation: Review or disable changes to .cursorrules, CLAUDE.md, and .antigravityrules before use, and inspect any modified instruction files before committing them. <br>
Risk: The skill scans projects, watches files, and maintains persistent local memory, which can capture sensitive project context if secrets are indexed. <br>
Mitigation: Avoid indexing directories that contain secrets, credentials, or private data, and periodically inspect or remove local .muninn memories and indexes. <br>
Risk: The scanner verdict is suspicious and the security guidance says to treat advertised version and build claims with caution. <br>
Mitigation: Verify the installed package and version in a disposable project before wider use, and only install it where local file scanning and instruction-file modification are acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/endgegnerbert-tech/muninn) <br>
- [Publisher profile](https://clawhub.ai/user/endgegnerbert-tech) <br>
- [Muninn homepage](https://www.muninn.space) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [MCP tool responses with Markdown memories and local configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local project indexes and memories; may update repository agent instruction files.] <br>

## Skill Version(s): <br>
2.3.7 (source: SKILL.md frontmatter, package.json, server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
