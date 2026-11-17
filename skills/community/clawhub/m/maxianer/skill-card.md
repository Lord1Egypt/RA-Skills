## Description:

中华术数推演系统（八字/紫微/六爻/梅花/奇门/称骨/铁板/解梦）。当用户提到算命/算八字/排八字/看命盘/紫微斗数/六爻/占卜/梅花易数/奇门遁甲/称骨/铁板神数/解梦/算一卦/帮我算算/看看运势/什么命/命理时触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xgimiapoll-code](https://clawhub.ai/user/xgimiapoll-code)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke this skill through an agent to collect birth, event, or dream details, call the publisher's divination service, and receive natural-language Chinese metaphysics readings or optional HTML reports. It is intended for astrology/divination-style interpretation workflows rather than factual, medical, legal, or financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal birth details, names, questions, dream descriptions, and generated reports may be sent to the publisher's remote service.

Mitigation: Use only with informed user consent and avoid entering sensitive personal data unless that transmission is acceptable.

Risk: The evidence reports plaintext HTTP transport and an embedded shared bearer token.

Mitigation: Prefer a deployment that uses HTTPS, validates the API host, and supplies a private API key through environment configuration.

Risk: Divination and health-related readings can be mistaken for authoritative advice.

Mitigation: Present outputs as interpretive or entertainment-oriented guidance and keep health disclaimers when discussing wellness topics.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Shell commands, Guidance]

**Output Format:** [Natural-language Chinese Markdown with script-invocation examples and optional HTML report output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote API responses may return JSON for agent interpretation; final user-facing readings should avoid exposing raw JSON field names.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
