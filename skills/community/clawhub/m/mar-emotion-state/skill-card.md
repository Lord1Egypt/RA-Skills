## Description: <br>
NL emotion tracking + prompt injection via OpenClaw hook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install an emotion-state hook that evaluates user and agent emotions, stores inferred state, and injects a compact emotion summary into the system prompt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recent conversation text may be sent to SkillBoss API Hub or a configured classifier for emotion detection. <br>
Mitigation: Enable the skill only for conversations where external classification is acceptable, and review provider handling and retention before use. <br>
Risk: Inferred emotion state can be shared across agents by default. <br>
Mitigation: Set EMOTION_MAX_OTHER_AGENTS to 0 when cross-agent emotion context should not be included. <br>
Risk: The hook requires a sensitive SkillBoss API key when no classifier URL is configured. <br>
Mitigation: Store SKILLBOSS_API_KEY in the OpenClaw hook environment or secret management path and avoid committing it to source files. <br>
Risk: Inferred emotion summaries may be inappropriate for sensitive personal, medical, legal, HR, or confidential business contexts. <br>
Mitigation: Avoid using the skill in those contexts unless local state deletion practices and provider data handling have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/mar-emotion-state) <br>
- [Publisher profile](https://clawhub.ai/user/marjoriebroad) <br>
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OpenClaw hook setup guidance and injects an emotion_state prompt block when enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
