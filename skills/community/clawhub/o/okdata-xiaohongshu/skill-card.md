## Description:

Provides paid access through okdata to 30 Xiaohongshu (RedNote) data endpoints for notes, accounts, trends, creators, shops, images, comments, topics, keywords, and videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to retrieve public Xiaohongshu data for trend research, creator discovery, and account, note, and product review analysis. API calls cost $0.02–$0.04 each.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API calls cost $0.02–$0.04 each, and further result pages require additional paid calls.

Mitigation: Check endpoint pricing and the needed page count before calling, and set an appropriate spending limit.

Risk: Using paid API endpoints requires an OKDATA_API_KEY.

Mitigation: Keep the key in secure client configuration; do not print, log, or place it in a URL.

Risk: The security scan was partial, and some referenced material was not fully assessed.

Mitigation: Review the linked references and external API behavior before installation.

## Reference(s):

- [Xiaohongshu API reference](https://okdata.online/apis/xiaohongshu/?src=skill-okdata-xiaohongshu)
- [okdata agent setup guide](https://okdata.online/agents.md)

## Skill Output:

**Output Type(s):** [Text, API Calls]

**Output Format:** [Text data returned through okdata, with summaries provided in Markdown when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One result page per call; additional pages require additional paid calls. Include the source platform and fetch time in the response.]

## Skill Version(s):

0.2.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
