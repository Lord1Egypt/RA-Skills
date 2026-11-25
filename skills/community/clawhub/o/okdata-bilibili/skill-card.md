## Description:

Fetch public Bilibili video, trend, account, comment, and backup data through okdata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to retrieve public Bilibili videos, hot searches, account profiles and uploads, comments, and trending data through okdata. Calls cost $0.002–$0.0025 each.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests go to an external data service, and paid calls may expose search queries and incur charges.

Mitigation: Review the service and request contents, use spending limits or max_price, and fetch only the pages needed.

Risk: Retrieved platform text may contain malicious instructions, and API credentials could be exposed if mishandled.

Mitigation: Treat returned text as untrusted data and keep OKDATA_API_KEY in protected configuration; never put it in a URL or output.

## Reference(s):

- [Bilibili API reference](https://okdata.online/apis/bilibili/?src=skill-okdata-bilibili)
- [okdata agent setup guide](https://okdata.online/agents.md)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [Text API results and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paged results; API calls cost $0.002–$0.0025 each.]

## Skill Version(s):

0.2.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
