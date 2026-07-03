## Description: <br>
Intent Engine classifies user requests for AI assistant routing using keyword, regex, weighted scoring, confidence values, dynamic intent management, and a web dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to classify user messages into code, knowledge, task, and chat intents, then route requests to appropriate downstream skills or workflows. It also provides a local dashboard and REST API for editing intents, testing classifications, and reviewing classification distribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local management service is unauthenticated and can modify persisted routing configuration. <br>
Mitigation: Add access control before using it on any shared machine or network. <br>
Risk: The service starts in debug mode on all network interfaces. <br>
Mitigation: Bind it to localhost and disable debug mode before deployment beyond a private local test environment. <br>
Risk: Intent import, edit, and delete features can change or remove routing data. <br>
Mitigation: Export or back up intent data before using import, edit, or delete features. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bettermen/intent-engine) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON API responses and dashboard-rendered text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Classification output can include category, sub-category, confidence score, matched keywords, matched patterns, routing skill, routing description, and alternative intents.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
