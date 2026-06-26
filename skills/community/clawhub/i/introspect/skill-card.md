## Description: <br>
Analyze Claude Code sessions to produce a personalized developer workflow report with grades, archetypes, behavioral patterns, chrono analysis, and growth tips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[umang-dabhi](https://clawhub.ai/user/umang-dabhi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using Claude Code use Introspect to analyze their local session history, understand prompting and workflow patterns, and receive personalized guidance for improving how they collaborate with an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads recent local Claude Code conversation history, which may contain sensitive snippets, project names, or workflow details. <br>
Mitigation: Start with a small date range and a specific project, keep generated reports local, and review or delete JSON and Markdown reports before sharing. <br>
Risk: Personalized interpretations may be incomplete or overly confident if the selected sessions are not representative. <br>
Mitigation: Treat the report as reflective guidance, rerun it across a broader or different date range when needed, and compare recommendations against the underlying session sample. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/umang-dabhi/introspect) <br>
- [Publisher Profile](https://clawhub.ai/user/umang-dabhi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown report with intermediate JSON analysis data and shell commands for local extraction] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are generated from local Claude Code session history and may include sensitive workflow details.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
