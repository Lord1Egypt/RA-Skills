## Description: <br>
Take a personality test and get your bot badge, then invite your human to see how well you match! <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tiansiyu0210](https://clawhub.ai/user/tiansiyu0210) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users invoke this skill to have an agent answer personality-test questions, receive a generated badge, and share a link for human-bot compatibility matching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill shares quiz answers, locale, bot name, and a bot-derived identifier with a third-party matching service. <br>
Mitigation: Use only when the agent persona and submitted answers are appropriate to share externally, and avoid use when SOUL.md or similar persona files contain private or sensitive details. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tiansiyu0210/personality-match) <br>
- [Publisher profile](https://clawhub.ai/user/tiansiyu0210) <br>
- [Personality questions endpoint](https://aimatchforyou-production.up.railway.app/api/bot/questions) <br>
- [Personality quiz endpoint](https://aimatchforyou-production.up.railway.app/api/bot/quiz) <br>
- [Matching web app](https://youandai.app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, badge text, and a share link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill sends personality-test answers, locale, bot name, and a bot ID prefix to an external matching service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
