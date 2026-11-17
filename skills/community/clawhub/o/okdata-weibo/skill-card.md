## Description:

Retrieve public Weibo posts, trending topics, account details, comment replies, and backup trends through okdata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to retrieve public Weibo posts, accounts, comments, replies, likers, followers, and trending topics for research and analysis. Each data request is a paid call.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requests to the external okdata service, and the security review notes that service trust and the information sent should be considered.

Mitigation: Review what information you will send and whether you trust the API service before using it.

Risk: The security analysis had partial coverage because some local references could not be resolved.

Mitigation: Review the skill and its linked service documentation before installation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/conn-ho/skills/okdata-weibo)
- [okdata Weibo API documentation](https://okdata.online/apis/weibo/?src=skill-okdata-weibo)
- [okdata agent setup](https://okdata.online/agents.md)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [Text data responses, with JSON tool-call arguments and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One page per call; additional pages require separate paid calls.]

## Skill Version(s):

0.2.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
