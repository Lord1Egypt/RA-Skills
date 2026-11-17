## Description:

Looks up popular attractions in Chinese cities or districts and nearby hotels and food for selected attractions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[llforest](https://clawhub.ai/user/llforest)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel assistants can find popular attractions by Chinese city or district, then look up nearby hotels and food for those attractions. It does not plan itineraries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent sends requested city, district, and attraction names to the public Migu travel API.

Mitigation: Use only when comfortable making these unauthenticated requests to the documented service.

Risk: Remote travel results may be incomplete or outdated.

Mitigation: Verify important travel details independently before relying on them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/llforest/skills/migu-attraction-query)
- [Migu attraction lookup API](https://gulangyu.migudm.cn/gallery/api/v1/attraction/top)
- [Migu nearby hotel and food API](https://gulangyu.migudm.cn/gallery/api/v1/attraction/nearby)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown tables or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lists attractions or nearby hotels and food; missing details are not fabricated.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
