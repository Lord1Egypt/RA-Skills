## Description: <br>
Delivers a daily 7 AM CDT briefing with local weather, one key healthcare revenue insight, Pittsburgh sports updates, and seasonal fantasy baseball news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j3m2b](https://clawhub.ai/user/j3m2b) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal automation users schedule Morning Brief to receive a compact daily message covering Mission, Kansas weather, one healthcare revenue cycle insight, Pittsburgh sports, and in-season fantasy baseball updates. <br>

### Deployment Geography for Use: <br>
United States, with local weather configured for Mission, Kansas and scheduling configured for America/Chicago. <br>

## Known Risks and Mitigations: <br>
Risk: The release bundles a Gmail IMAP helper that can read a Gmail inbox when credentials are provided. <br>
Mitigation: Review before installing; do not provide Gmail credentials or run email_briefing.py unless inbox access is explicitly intended. <br>
Risk: The bundled Gmail helper is not described by the public Morning Brief behavior. <br>
Mitigation: Treat the helper as out-of-scope until the publisher documents, scopes, or removes it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/j3m2b/jb-morning-brief) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [Short Markdown-style briefing message with optional cron configuration JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Keep the briefing under 300 words, lead with weather, include only one RCM insight, prioritize upcoming sports, and skip fantasy baseball when out of season.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
