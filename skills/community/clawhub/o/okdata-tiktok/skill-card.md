## Description:

Retrieves public TikTok video, account, advertising, shop, comment, reply, transcript, and hashtag data through okdata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve public TikTok content, account metrics, advertising, shop listings and reviews, comments, replies, captions, and hashtag videos for research and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests use the external service at api.okdata.online, and the security scan was partly incomplete.

Mitigation: Use the service only when it is trusted and appropriate for the requested data; review unresolved local references before installation.

Risk: Paid API calls can incur charges, including calls that reach a data source but fail or return no results.

Mitigation: Tell the user the maximum cost before the first paid call, set a per-call price cap, and fetch only the pages needed.

Risk: API credentials could be exposed if included in output, logs, or request URLs.

Mitigation: Keep the key in a secret or client configuration and never print, log, or place it in a URL.

## Reference(s):

- [TikTok API documentation](https://okdata.online/apis/tiktok/?src=skill-okdata-tiktok)
- [okdata agent setup guide](https://okdata.online/agents.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Text data with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are paginated; each API call retrieves one page. Documented per-call prices range from $0.002 to $0.004.]

## Skill Version(s):

0.2.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
