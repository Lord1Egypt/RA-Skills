## Description: <br>
Proactive screen context processor triggered by screen.context payloads; it analyzes visual content, applies the configured persona mode, and decides whether an observation warrants a proactive notification to the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fikriaf](https://clawhub.ai/user/fikriaf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agent builders use Openweruh to process screen.context events and decide whether to send concise, persona-specific interventions for skepticism, research support, focus, breaks, or silent summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can analyze active screen content, which may expose sensitive personal or work information. <br>
Mitigation: Enable it only after confirming how screen events are turned on, how observations are stored, how long they are retained, and how to pause or delete them. <br>
Risk: Silent mode records context for later summaries without immediate notifications. <br>
Mitigation: Confirm that silent mode is intentional, visible to the user, and compatible with the user's privacy expectations before deployment. <br>
Risk: Persona modes may send proactive nudges that interrupt the user or misread screen context. <br>
Mitigation: Keep intervention thresholds conservative and review generated messages for relevance, tone, and accuracy before broad use. <br>


## Reference(s): <br>
- [OpenWeruh Modes](artifact/references/modes.md) <br>
- [OpenWeruh Response Examples](artifact/references/examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/fikriaf/openweruh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Concise Markdown notification text or no user-facing response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Intervention messages start with [👁️ OpenWeruh] and are limited to under two sentences when a notification is warranted.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
