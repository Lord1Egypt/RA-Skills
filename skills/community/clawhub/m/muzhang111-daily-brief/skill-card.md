## Description: <br>
Provides a concise daily brief with Nantong weather and the top five V2EX hot posts when requested or on an intentional morning schedule. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muzhang111](https://clawhub.ai/user/muzhang111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users use this skill to generate a short morning briefing that combines current Nantong weather with a quick scan of V2EX hot posts. It is suitable for lightweight personal or team status briefings, not professional weather forecasting or long-form news coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public wttr.in and V2EX endpoints, so results depend on external service availability and current public content. <br>
Mitigation: Handle fetch failures explicitly and tell the user when weather or hot-post data is unavailable instead of filling gaps with unsupported content. <br>
Risk: A scheduled 8:00 AM run or broad trigger phrase could generate a brief when the user did not intend it. <br>
Mitigation: Enable scheduled execution only after user confirmation and use specific trigger phrases for on-demand briefs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/muzhang111/muzhang111-daily-brief) <br>
- [Publisher profile](https://clawhub.ai/user/muzhang111) <br>
- [wttr.in Nantong weather endpoint](https://wttr.in/Nantong?format=3) <br>
- [V2EX hot topics API](https://www.v2ex.com/api/topics/hot.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown brief with a weather line and numbered V2EX post list] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public wttr.in and V2EX data; outputs the first five hot posts with titles and node names.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
