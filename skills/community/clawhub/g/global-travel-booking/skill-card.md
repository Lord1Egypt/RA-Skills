## Description:

全球旅行预订 helps agents aggregate hotel search, room, pricing, and booking information across providers such as 分贝通, 携程, 美团, 同程, 华住会, and 锦江.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-zry](https://clawhub.ai/user/ryan-zry)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel agents use this skill to search hotels across multiple travel platforms, compare source-specific prices, and format aggregated hotel results for review before booking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release overstates live hotel search, room-detail, and booking capabilities compared with the implemented integrations.

Mitigation: Do not rely on it for real prices, availability, room details, or bookings until provider integrations, consent flow, and booking controls are implemented and documented.

Risk: Provider credentials or booking access could be granted before operational safeguards are in place.

Mitigation: Avoid broad provider credentials and use limited test access until integration behavior and booking approval controls have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-zry/skills/global-travel-booking)
- [Fenbeitong API endpoint](https://openapiv2.fenbeitong.com)
- [Ctrip API endpoint](https://api.ctrip.com)
- [Meituan API endpoint](https://api.meituan.com)
- [Tongcheng API endpoint](https://api.tongcheng.com)
- [Huazhu API endpoint](https://api.huazhu.com)
- [Jinjiang API endpoint](https://api.jinjiang.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Code, Guidance]

**Output Format:** [Markdown tables and JSON-like API result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve provider-supplied hotel, price, availability, and source information without inventing missing data.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
