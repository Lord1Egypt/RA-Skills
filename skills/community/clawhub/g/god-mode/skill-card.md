## Description: <br>
Developer oversight and AI agent coaching for viewing project status across repositories, syncing GitHub data, and analyzing agents.md against commit patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[InfantLab](https://clawhub.ai/user/InfantLab) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to track activity across configured repositories, refresh GitHub project data, and generate agent-instruction improvement suggestions from commit patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads configured repositories through the user's existing GitHub CLI login and caches repository activity plus agent-instruction content locally. <br>
Mitigation: Install and run it only for repositories you are comfortable exposing to the local ~/.god-mode cache, and review local cache handling before use on shared systems. <br>
Risk: Agent analysis may display prompt content and repository-derived context in the terminal. <br>
Mitigation: Avoid running agent analysis in CI logs or shared terminals unless the generated output can be exposed there. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/InfantLab/god-mode) <br>
- [GitHub repository referenced by artifact documentation](https://github.com/InfantLab/god-mode-skill) <br>
- [GitHub CLI documentation](https://cli.github.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, JSON, and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires gh, sqlite3, and jq; stores repository activity and agent-instruction analysis locally under ~/.god-mode.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
