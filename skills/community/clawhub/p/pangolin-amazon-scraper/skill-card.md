## Description: <br>
Scrape Amazon product data using Pangolin APIs for product lookup, keyword search, rankings, reviews, pricing, regional comparison, category browsing, and seller research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuyu020923](https://clawhub.ai/user/liuyu020923) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve and summarize structured Amazon product, ranking, review, seller, and regional pricing data through Pangolin APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Pangolin credentials and may store a persistent API key in the user's home directory. <br>
Mitigation: Prefer a scoped API key, avoid shared environments, and rotate or delete ~/.pangolin_api_key when access is no longer needed. <br>
Risk: The security review marked this release for manual review because credential handling is central to normal operation. <br>
Mitigation: Review the skill before installing and only grant credentials in environments where local credential storage is acceptable. <br>


## Reference(s): <br>
- [Pangolin](https://www.pangolinfo.com) <br>
- [Amazon API reference](references/amazon-api.md) <br>
- [Output schema](references/output-schema.md) <br>
- [Error codes](references/error-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and structured JSON results from the Pangolin API.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Pangolin credentials or an API key; supports multiple Amazon regions, parser modes, and review pagination.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
