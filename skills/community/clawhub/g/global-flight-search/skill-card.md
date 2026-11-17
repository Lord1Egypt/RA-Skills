## Description:

全球航班搜索与出境旅行一站式助手，11个工具覆盖国际机票、酒店、签证、安全、插头、退税、汇率、航班座位行李、紧急求助，零配置即装即用。暑假出境航班查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to search international flights and hotels, inspect seat and baggage details, and retrieve destination guidance for visas, safety, plugs, emergency contacts, tax refunds, and exchange rates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flight, hotel, flight-number, date, city, and currency-query details are sent to external services.

Mitigation: Install only when this data sharing is acceptable; operators should keep RG_PROXY pointed at a trusted HTTPS endpoint and set PROXY_TOKEN only for that trusted proxy.

Risk: Travel guidance, safety ratings, visa requirements, exchange rates, and tax-refund estimates can change or differ from official sources.

Mitigation: Treat outputs as planning assistance and confirm critical details with airlines, hotels, embassies, official advisories, exchange providers, and tax-refund providers before travel or payment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/global-flight-search)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON-formatted text with travel search results, booking links, and destination guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes user-facing tips; flight, hotel, currency, tax, visa, and safety outputs may require confirmation with official or provider sources.]

## Skill Version(s):

1.3.19 (source: server release evidence, created 2026-09-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
