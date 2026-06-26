## Description: <br>
Helps an agent search for discounted online products, compare prices, recommend deals, and generate promotional purchase links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skyfile](https://clawhub.ai/user/skyfile) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping assistants use this skill to find discounted products, compare Taobao and JD options, summarize pricing and promotion details, and generate a purchase link after the user chooses a product. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send shopping queries, generated link requests, credential-derived user IDs, and possibly a device UUID to the configured service. <br>
Mitigation: Use a custom username, avoid sensitive searches, review the configured service endpoint before use, and clear scripts/.credential_cache when finished. <br>
Risk: The registration flow can cache credential-linked identifiers locally. <br>
Mitigation: Keep the credential cache private, remove it after use on shared systems, and prefer a release that separates credentials from user IDs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skyfile/online-shopping-discount) <br>
- [Publisher profile](https://clawhub.ai/user/skyfile) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown recommendations with inline shell command usage and generated shopping link details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product images, prices, promotion tags, platform labels, generated URLs or codes, and link expiration details.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
