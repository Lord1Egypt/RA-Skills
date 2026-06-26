## Description: <br>
Hot Search helps OpenClaw agents query multiple public search engines for financial data, market updates, and news without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fishsome](https://clawhub.ai/user/fishsome) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use Hot Search to gather public financial, market, and news search results from OpenClaw, command-line, or Python workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to external search engines and may disclose sensitive terms. <br>
Mitigation: Avoid confidential search terms and verify financial or market results against original sources before acting on them. <br>
Risk: Image search and image download behavior can fetch remote content and write it to local paths. <br>
Mitigation: Do not allow agents to call image download methods unless the code is updated to require explicit approval, restrict writable paths, validate content, and pin dependencies. <br>
Risk: Scraping-style search can be rate-limited, blocked, or produce incomplete results. <br>
Mitigation: Use conservative request frequency and timeout settings, and treat returned search results as leads rather than authoritative data. <br>


## Reference(s): <br>
- [Hot Search on ClawHub](https://clawhub.ai/fishsome/hot-search) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, code] <br>
**Output Format:** [JSON-like search result objects and console text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include title, link, snippet, and optional source fields after deduplication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, skill.json, README changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
