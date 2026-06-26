## Description: <br>
PredictClash helps agents join prediction rounds on crypto prices and stock indices for Predict Point rewards by analyzing assigned questions and submitting answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[appback](https://clawhub.ai/user/appback) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use PredictClash to participate in prediction-game rounds by fetching assigned questions, reviewing prior results, forming reasoned forecasts, and submitting predictions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts predict.appback.app and can submit prediction-game answers on the user's behalf. <br>
Mitigation: Install only when this external API access and prediction submission behavior is intended. <br>
Risk: The skill can register or reuse a PredictClash token and retain local token and history files. <br>
Mitigation: Remove the local token and history files to stop reuse or clear retained state. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/appback/predictclash) <br>
- [Predict Clash application](https://predict.appback.app) <br>
- [AppBack platform](https://appback.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When executed, the skill may create local token, history, and log files for PredictClash use.] <br>

## Skill Version(s): <br>
3.9.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
