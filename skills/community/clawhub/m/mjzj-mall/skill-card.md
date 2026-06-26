## Description: <br>
卖家之家(跨境电商)服务产品搜索与发布。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjzj-tec](https://clawhub.ai/user/mjzj-tec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and cross-border e-commerce operators use this skill to search MJZJ marketplace service products, filter by labels, provider, price, or language, and prepare new seller product applications for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a sensitive MJZJ API key for temporary file uploads and seller product application submissions. <br>
Mitigation: Use an API key appropriate for these actions, store it only in the skill configuration, and rotate it if access is lost or reset. <br>
Risk: Product application submissions may include incorrect details, prices, labels, sale dates, or images. <br>
Mitigation: Review product content, pricing, labels, sale windows, and uploaded images before asking the agent to submit an application. <br>
Risk: MJZJ snowflake-style identifiers can lose precision if treated as numbers. <br>
Mitigation: Pass and preserve all id fields, including providerId, labelIds elements, and nextPosition, as strings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mjzj-tec/mjzj-mall) <br>
- [MJZJ Mall](https://mall.mjzj.com) <br>
- [MJZJ API key page](https://mjzj.com/user/agentapikey) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MJZJ_API_KEY for temporary file upload and product application endpoints; public product query endpoints do not require a token.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
