## Description: <br>
Search and compare grocery prices and promotions in Austria and Germany via the Preisrunter API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidus05](https://clawhub.ai/user/davidus05) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and shopping assistants use this skill to search Austrian and German grocery prices, promotions, supermarket availability, and product detail links through the Preisrunter API. <br>

### Deployment Geography for Use: <br>
Austria and Germany <br>

## Known Risks and Mitigations: <br>
Risk: Grocery search terms, region choices, and shop filters are sent to api.preisrunter.net. <br>
Mitigation: Avoid entering personal or sensitive information in search terms, and use the skill only when sharing those queries with the Preisrunter API is acceptable. <br>
Risk: Unencoded query parameters can produce incorrect requests or expose unintended parameter values. <br>
Mitigation: URL-encode search terms and shop filters before running curl commands. <br>
Risk: The upstream API can rate-limit requests or return no results. <br>
Mitigation: Avoid aggressive polling and handle HTTP 429 and HTTP 404 responses gracefully. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/davidus05/preisrunter) <br>
- [Preisrunter homepage](https://preisrunter.at) <br>
- [Preisrunter OpenClaw API wrapper](https://api.preisrunter.net/wrapper/openclaw-v1/products/) <br>
- [Publisher profile](https://clawhub.ai/user/davidus05) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, JSON data, text] <br>
**Output Format:** [Markdown guidance with curl and jq examples, plus JSON product responses from the Preisrunter API.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key is required; queries may include search terms, region, sale-only filtering, and shop filters.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
