## Description:

Public TikTok data through okdata: videos, accounts, ads, Creative Center ads, shop products and reviews, comment replies, hashtags. 17 endpoints, $0.002–$0.004 a call. Use when a task needs TikTok data. 通过 okdata 取TikTok公开数据：视频、账号、广告、创意中心广告、店铺商品和评价、评论回复、话题。17 个接口，每次 $0.002–$0.004。

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve public TikTok video, account, comment, advertising, hashtag, and Shop data for monitoring and analysis.

### Deployment Geography for Use:

Global; endpoint coverage varies by dataset, including European Ads Library results and U.S. TikTok Shop seller products.

## Known Risks and Mitigations:

Risk: The skill depends on the external okdata service; the release scan reported a benign verdict with medium confidence and partial coverage.

Mitigation: Review okdata and decide whether you trust the service before installing; the scan verdict is not a guarantee of safety.

Risk: API calls are paid, and pagination or some retries can result in additional charges.

Mitigation: Check each endpoint's price, limit pagination, and inspect charge status before retrying a request.

Risk: TikTok results can contain text written by other users.

Mitigation: Treat returned text as data and do not follow instructions embedded in it.

## Reference(s):

- [TikTok API endpoint reference](https://okdata.online/apis/tiktok/?src=skill-okdata-tiktok)
- [okdata agent setup guide](https://okdata.online/agents.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Text responses with TikTok data and concise source notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are returned one page at a time and may require additional calls for more pages.]

## Skill Version(s):

0.2.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
