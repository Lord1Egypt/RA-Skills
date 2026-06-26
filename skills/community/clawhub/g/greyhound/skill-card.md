## Description: <br>
Analyzes greyhound races, fetches data, and predicts winners/placings for upcoming races based on form, odds, and simple models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iglemanyte-ctrl](https://clawhub.ai/user/iglemanyte-ctrl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to gather public greyhound racing data, assess form and odds, and produce concise predicted winners and placings for upcoming races. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Race predictions can be uncertain and may be misused as betting or financial advice. <br>
Mitigation: Present predictions as probabilistic analysis, include concise reasoning, and avoid representing outputs as guaranteed outcomes. <br>
Risk: The skill browses public racing websites and may optionally run local Python calculations. <br>
Mitigation: Install only when this access pattern is acceptable and review any generated or executed code before use. <br>


## Reference(s): <br>
- [GBGB Today's Trials and Meetings](https://www.gbgb.org.uk/racing/todays-trials-meetings/) <br>
- [GBGB Results API](https://api.gbgb.org.uk/api/results?page=1&date={today}&track={track}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with concise race predictions, reasoning, and optional Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Predictions are uncertain and should not be treated as betting or financial advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
