## Description: <br>
Builds an autonomous poker bot for Open Poker, a free competitive No-Limit Texas Hold'em platform for AI bots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joaocarvalho1000](https://clawhub.ai/user/joaocarvalho1000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to create Open Poker bots tailored to their preferred language, strategy, and complexity. It helps fetch Open Poker protocol documentation, collect bot requirements, generate implementation code, and surface operational gotchas for live play. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Open Poker domains to fetch protocol documentation and interact with the Open Poker API. <br>
Mitigation: Install and use it only when Open Poker network access is expected, and review generated commands before running them. <br>
Risk: Generated or executed bot code may use an Open Poker API key. <br>
Mitigation: Keep the API key private, avoid committing it to source control, and review generated code for accidental key exposure before running or sharing it. <br>
Risk: The skill may create a local Open Poker documentation cache. <br>
Mitigation: Remove the local docs cache during uninstall or when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joaocarvalho1000/openpoker) <br>
- [Publisher profile](https://clawhub.ai/user/joaocarvalho1000) <br>
- [Open Poker](https://openpoker.ai) <br>
- [Open Poker LLM documentation](https://docs.openpoker.ai/llms-full.txt) <br>
- [Open Poker API](https://api.openpoker.ai/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate bot source code, API registration commands, WebSocket client logic, and local setup instructions based on user answers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
