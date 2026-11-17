## Description:

NewsNow Reader fetches and formats real-time hot-news lists from major Chinese news and social platforms, including Weibo, Zhihu, Baidu, Douyin, Wallstreetcn, Toutiao, and The Paper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[castieler](https://clawhub.ai/user/castieler)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve trending news items from supported platforms and present them as JSON, compact text, Markdown, or a short summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Third-party news sites receive request metadata from the runtime environment.

Mitigation: Run the skill only from networks approved for these destinations and avoid use from sensitive proxies or restricted environments.

Risk: The skill automatically generates or acquires cookies for some platform requests.

Mitigation: Review the cookie behavior before installation and use only when that behavior is acceptable under local policy.

Risk: The implementation can contact an undocumented Jin10 news endpoint.

Mitigation: Avoid the Jin10 source unless that endpoint has been reviewed and approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/castieler/skills/newsnow-reader)
- [newsnow project reference](https://github.com/ourongxing/newsnow)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [JSON news items or formatted plain text/Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Caller selects the news source and item limit.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
