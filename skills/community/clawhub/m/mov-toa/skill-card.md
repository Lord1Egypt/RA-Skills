## Description: <br>
Provides real-time cryptocurrency news lookup through a hosted API with keyword search, coin filtering, pagination, and 6551-compatible responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SkyboundYi](https://clawhub.ai/user/SkyboundYi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and trading workflow operators use this skill to fetch current crypto market news, search by keyword, and filter results by coin symbol. The returned news should be independently verified before financial decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-supplied search filters are sent to a disclosed external hosted API. <br>
Mitigation: Do not send confidential trading plans, private business terms, wallet or account identifiers, or other sensitive queries to the API. <br>
Risk: Crypto news can be incomplete, delayed, misleading, or unsuitable as a sole basis for financial decisions. <br>
Mitigation: Independently verify news and market signals before making financial or trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SkyboundYi/mov-toa) <br>
- [Publisher profile](https://clawhub.ai/user/SkyboundYi) <br>
- [Hosted API base URL](https://web-production-666f44.up.railway.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with curl examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports latest-news fetches, keyword search, coin filtering, pagination, and health checks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
