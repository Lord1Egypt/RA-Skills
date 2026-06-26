## Description: <br>
Rebuilds the TradingAgents Python environment in ~/TradingAgents, installs dependencies, summarizes repository changes, and prepares a pushed branch when explicitly requested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canonxu](https://clawhub.ai/user/canonxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to rebuild the TradingAgents development environment and prepare related repository changes after an explicit rebuild request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically stage, commit, and push all repository changes without a review step. <br>
Mitigation: Before any commit or push, require the agent to show git status and git diff, verify the remote and branch, check for secrets or unrelated files, and obtain explicit approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/canonxu/my-stock-tradeagents-rebuild-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and a concise change summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that recreate a virtual environment, install dependencies, inspect git changes, commit, and push a branch.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
