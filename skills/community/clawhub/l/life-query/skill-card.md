## Description:

Life Query helps an agent answer everyday lookup requests for parcel tracking, currency conversion and historical exchange rates, China fuel prices, and global weather forecasts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eamanc-lab](https://clawhub.ai/user/eamanc-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route natural-language daily-life questions into lookup commands for package status, exchange rates, China gas prices, and weather. It is useful when an agent needs current public-service data and should return concise JSON, table text, or user-facing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup inputs may be sent to disclosed external services, including parcel numbers, city names, currency inputs, and province queries.

Mitigation: Use the skill only when those query details are appropriate to share with the listed services, and configure direct Kuaidi100 credentials when avoiding the free parcel proxy is important.

Risk: The documentation shows unpinned ClawHub install and update commands.

Mitigation: Prefer pinned installer and update versions in controlled environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/eamanc-lab/skills/life-query)
- [Project Homepage](https://github.com/eamanc-lab/life-query)
- [Frankfurter Exchange Rate API](https://api.frankfurter.app)
- [Kuaidi100 Parcel Query Endpoint](https://poll.kuaidi100.com/poll/query.do)
- [Eastmoney Oil Price Data](https://data.eastmoney.com/cjsj/oil_default.html)
- [wttr.in Weather Service](https://wttr.in)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON by default, plain-text tables on request, and Markdown guidance around results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and python3; optional Kuaidi100 credentials can route parcel tracking through the user's direct provider account.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
