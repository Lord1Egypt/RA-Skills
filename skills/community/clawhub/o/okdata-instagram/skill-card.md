## Description:

Fetch public Instagram account, post, comment, hashtag, and reel transcript data through okdata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

People analyzing public Instagram accounts and content can retrieve profile, post, comment, hashtag, and reel transcript data through okdata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on the external okdata service, and the security review reports that reference checks were partial.

Mitigation: Review the service documentation and decide whether its data handling fits the task; keep the API key in protected configuration and do not expose it in logs or URLs.

Risk: Endpoint calls are paid, including calls that reach a data source but fail or return no results.

Mitigation: Tell the user the intended call and maximum cost before the first paid request, cap spending, and request extra pages only when needed.

## Reference(s):

- [Instagram API reference](https://okdata.online/apis/instagram/?src=skill-okdata-instagram)
- [okdata agent setup guide](https://okdata.online/agents.md)

## Skill Output:

**Output Type(s):** [Text, API Calls, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Text results and Markdown instructions with JSON and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paged data; each additional page requires another API call.]

## Skill Version(s):

0.2.3 (source: server-resolved ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
