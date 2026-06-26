## Description: <br>
Openclaw Free Search lets OpenClaw agents run web searches through a free DuckDuckGo-based search script without requiring Brave or Perplexity API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent developers use this skill to run web searches when paid search provider API keys are not configured. It is suited for general information lookup where sharing the query with DuckDuckGo is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to DuckDuckGo and may expose sensitive information in queries. <br>
Mitigation: Do not use the skill for passwords, API keys, private project names, customer data, or other sensitive information; review queries before execution. <br>
Risk: The search script may fall back to curl when direct fetch fails, so results depend on local outbound network and proxy behavior. <br>
Mitigation: Use it only in environments where outbound access to DuckDuckGo and the host proxy configuration are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/openclaw-free-search) <br>
- [DuckDuckGo Instant Answer API endpoint](https://api.duckduckgo.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [Plain text search results by default, or JSON when the --json flag is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns an abstract and up to 10 related results when available; exits nonzero on search or parse failure.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
