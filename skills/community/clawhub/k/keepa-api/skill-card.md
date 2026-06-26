## Description: <br>
Keepa API client for querying Amazon product details, price history, sales rank history, search results, and best seller listings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boyd4y](https://clawhub.ai/user/boyd4y) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and Amazon marketplace analysts use this skill to query Keepa for ASIN product data, price history, sales ranks, keyword search results, and category best seller data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Keepa API key that may be stored in local configuration and sent as a request URL parameter. <br>
Mitigation: Prefer the KEEPA_API_KEY environment variable, keep configuration files out of shared repositories, avoid sharing command output that includes request URLs, and rotate the key if it is exposed. <br>
Risk: Keepa API usage consumes account tokens and can hit plan or rate limits. <br>
Mitigation: Confirm query scope before execution, batch requests only when needed, and monitor Keepa token usage for the configured account. <br>


## Reference(s): <br>
- [Keepa API reference](artifact/references/api-docs.md) <br>
- [Keepa API Documentation](https://keepa.com/#!api) <br>
- [Keepa Category Tree](https://keepa.com/#!category) <br>
- [Keepa API Examples](https://github.com/keepacom/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, and table or JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and a user-provided Keepa API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
