## Description:

Kamis Cli helps agents use the official KAMIS OpenAPI for Korean agricultural, livestock, and aquatic wholesale and retail price lookup, trend comparison, regional comparison, and code lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, restaurants, buyers, reporters, content creators, and agent developers use this skill to retrieve and compare Korean food and produce market prices, including daily spot checks, period trends, monthly and yearly averages, regional comparisons, and local code lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that configured KAMIS credentials can be sent to an arbitrary endpoint if the endpoint override is used.

Mitigation: Review before installing with real KAMIS credentials, run only in a trusted shell environment, leave KAMIS_BASE unset unless you control the endpoint, avoid shell tracing or command logging, and rotate the KAMIS key if it may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chloepark85/skills/kamis-cli)
- [KAMIS](https://www.kamis.or.kr)
- [KAMIS OpenAPI](https://www.kamis.or.kr/customer/reference/openapi_list.do)
- [KAMIS price API endpoint](https://www.kamis.or.kr/service/price/xml.do)
- [KAMIS local code table](reference/codes.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON responses, Markdown summaries, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Most live data calls require KAMIS credentials; TEST credentials are limited.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
