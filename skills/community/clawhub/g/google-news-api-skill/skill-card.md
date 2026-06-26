## Description: <br>
This skill helps agents retrieve structured Google News results through BrowserAct, including headlines, sources, publication times, article links, and optional authors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phheng](https://clawhub.ai/user/phheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts can use this skill to collect Google News results for topic monitoring, market research, PR tracking, competitor intelligence, daily summaries, and breaking-news review. The skill is intended for intentional third-party news collection using a BrowserAct API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: News search terms and task parameters are sent to BrowserAct for third-party collection. <br>
Mitigation: Use the skill only for intentional news collection and avoid sending sensitive or confidential search terms. <br>
Risk: The skill requires a BrowserAct API key and the security guidance flags unsafe key handling as a concern. <br>
Mitigation: Configure BROWSERACT_API_KEY through a secure environment variable or secret manager and do not paste the key into chat. <br>
Risk: The security verdict is suspicious due to broad automatic third-party use. <br>
Mitigation: Review the intended collection scope before execution and keep use limited to the user's requested news-gathering task. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/phheng/google-news-api-skill) <br>
- [BrowserAct Console](https://www.browseract.com/reception/integrations) <br>
- [BrowserAct Workflow API](https://api.browseract.com/v2/workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text containing status logs and structured news result fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and BROWSERACT_API_KEY; accepts search keywords, publish-date filter, and item limit.] <br>

## Skill Version(s): <br>
0.1.3 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
