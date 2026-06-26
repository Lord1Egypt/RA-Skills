## Description: <br>
Use when receiving code review feedback - requires technical verification before implementing suggestions, with reasoned pushback when feedback is technically questionable; no performative agreement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill when responding to code review feedback. It guides them to verify suggestions against the codebase, ask clarifying questions, push back on technically unsound changes, and implement validated fixes with tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to inspect and modify project code when review feedback is provided. <br>
Mitigation: Review the resulting changes and tests before merging, and require the agent to validate feedback against the codebase before implementation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/axelhu/openclaw-receiving-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, code, shell commands] <br>
**Output Format:** [Markdown or plain text guidance with code, commands, and test notes when implementation is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external services, credentials, MCP tools, or API keys are required by the skill evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
