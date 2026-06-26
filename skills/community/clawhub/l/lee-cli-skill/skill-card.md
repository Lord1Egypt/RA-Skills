## Description: <br>
Lee-CLI Skill helps an agent run the lee-cli personal assistant for weather jokes, news digests, work summaries, AI learning resource recommendations, and smart todo lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leeking001](https://clawhub.ai/user/leeking001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for personal productivity assistance, including daily briefings, work review, learning recommendations, and task planning. The skill is most useful when the lee-cli binary is installed and the required API credentials are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read Claude Code activity records and may use calendar or work context. <br>
Mitigation: Install and run it only when the lee-cli binary is trusted, and keep invocation scoped to explicit user requests. <br>
Risk: Weather, news, and Anthropic API calls may share request data with external services. <br>
Mitigation: Avoid including sensitive work details in prompts or command arguments, and treat command execution as external data sharing unless runtime documentation proves otherwise. <br>
Risk: API-key troubleshooting can expose secrets if an agent prints environment variables. <br>
Mitigation: Do not ask the agent to echo API keys; verify credential presence without displaying secret values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leeking001/lee-cli-skill) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Security notice](artifact/SECURITY.md) <br>
- [User guide](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent output may summarize or interpret lee-cli command results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
