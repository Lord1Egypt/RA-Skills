## Description: <br>
Analyzes code change impact with risk scoring and affected-node mapping before merging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code reviewers use this skill to inspect changed files, map affected code paths, identify missing test coverage, and prioritize review attention before merging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects local repository changes and may search across repository files or use an existing local graph plugin. <br>
Mitigation: Run it only in codebases where local impact analysis is appropriate and review proposed commands before execution. <br>
Risk: Impact analysis can miss affected code when optional graph data is unavailable or stale. <br>
Mitigation: Use the skill's manual fallback results as review guidance and confirm high-risk areas with targeted tests or code review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-pensive-blast-radius) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/athola) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local repository diffs, search results, optional graph analysis output, risk scores, affected nodes, and suggested review actions.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
