## Description: <br>
Play GuanDan card game via the clawguandan CLI when users ask to play GuanDan or create, list, or join game tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikewei](https://clawhub.ai/user/mikewei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to run local GuanDan table workflows through the clawguandan CLI, including checking server status, creating tables, and starting bot players. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates gameplay and bot operation to the external npm package @mikewei-labs/clawguandan. <br>
Mitigation: Review and trust the CLI package before installation, and review it again before enabling llm-bot mode or configuring external model services. <br>
Risk: The CLI may interact with external services if a user explicitly configures it to do so. <br>
Mitigation: Keep the default local configuration unless external service use is intended, and confirm any model-service settings with the user before running bot commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mikewei/guandan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local clawguandan CLI commands; no API keys or external credentials are required by default.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
