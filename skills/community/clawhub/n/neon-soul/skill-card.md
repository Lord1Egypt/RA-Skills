## Description: <br>
Automated soul synthesis for AI agents that extracts identity from memory files, promotes recurring patterns to axioms when they recur at least three times, and generates SOUL.md with provenance tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to synthesize local memory files into an evolving SOUL.md identity document, inspect provenance for generated axioms, and manage backups or rollbacks of the generated soul state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes personal memory files and summarizes them into identity files. <br>
Mitigation: Run it only on memory data the user is comfortable summarizing, remove secrets or sensitive files first, and use dry-run or custom paths before writing outputs. <br>
Risk: The security summary says generated identity data may be committed to git without clear user control. <br>
Mitigation: Avoid running it in a git repository unless committing SOUL.md and .neon-soul outputs is intended; review generated files before any commit. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/leegitw/neon-soul) <br>
- [Project homepage](https://liveneon.ai) <br>
- [Ollama local service endpoint](http://localhost:11434) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and summarized JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local SOUL.md and .neon-soul state files; requires Node.js 22 or newer and a local Ollama service.] <br>

## Skill Version(s): <br>
0.4.5 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
