## Description: <br>
Analyze any project directory and produce a detailed report covering what the project does, its tech stack, folder structure, entry points, how to run it, and where to start reading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[g30tr1x](https://clawhub.ai/user/g30tr1x) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to orient themselves in unfamiliar codebases by scanning a local project directory and receiving a concise report on purpose, stack, structure, entry points, and run commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and summarizes files from the selected project directory, which may include private code or sensitive local content. <br>
Mitigation: Run it only on an explicit directory, avoid workspaces containing secrets or unrelated private files, and review the report before sharing it outside your environment. <br>
Risk: Project summaries, detected entry points, and run commands may be incomplete or inaccurate for unusual repository layouts. <br>
Mitigation: Treat the report as orientation guidance and verify important commands or architectural conclusions against the source files before acting on them. <br>


## Reference(s): <br>
- [Project Analyzer on ClawHub](https://clawhub.ai/g30tr1x/pal) <br>
- [Publisher profile](https://clawhub.ai/user/g30tr1x) <br>
- [Python 3 downloads](https://www.python.org/downloads/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report based on local scanner output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and reads files from the target project directory selected by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
