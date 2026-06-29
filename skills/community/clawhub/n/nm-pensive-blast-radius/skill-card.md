## Description: <br>
Analyzes code change impact with risk scoring and affected-node mapping before merging to show what a change touches and what lacks test coverage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill before merging code changes to identify affected functions or files, assess risk drivers such as missing tests or security-sensitive logic, and choose follow-up review or test actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects local repository contents through git diff and search commands, and may invoke a locally installed gauntlet graph-query helper. <br>
Mitigation: Use it only in repositories where local code inspection by the agent is acceptable, and review optional helper commands before running them. <br>
Risk: Manual rg or grep fallback can produce noisy impact results because it searches by filename stem across file types. <br>
Mitigation: Treat fallback results as review guidance, narrow searches by language where appropriate, and confirm affected call sites before acting. <br>
Risk: Graph-based impact analysis depends on an available and current graph database. <br>
Mitigation: Build or refresh the gauntlet graph before relying on graph results, and use the manual fallback when graph data is unavailable. <br>


## Reference(s): <br>
- [Nm Pensive Blast Radius on ClawHub](https://clawhub.ai/athola/skills/nm-pensive-blast-radius) <br>
- [Pensive homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with risk tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local git diff, a gauntlet graph-query helper, sem, rg, or grep depending on repository tooling.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
