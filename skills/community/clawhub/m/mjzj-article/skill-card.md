## Description: <br>
卖家之家(跨境电商)资讯搜索与发布 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjzj-tec](https://clawhub.ai/user/mjzj-tec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External MJZJ users and content teams use this skill to search cross-border e-commerce articles and prepare or publish MJZJ articles through the service APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated endpoints can manage or publish content for the MJZJ account associated with MJZJ_API_KEY. <br>
Mitigation: Keep MJZJ_API_KEY private and review author identity, tags, article HTML, images, and publish time before publishing. <br>
Risk: Untrusted HTML or remote media could introduce unwanted content into published articles. <br>
Mitigation: Avoid importing HTML or media from untrusted sources and verify image transfer results before submitting the article. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mjzj-tec/mjzj-article) <br>
- [MJZJ homepage](https://mjzj.com) <br>
- [MJZJ agent API key page](https://mjzj.com/user/agentapikey) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with API endpoint and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated management and publishing flows require MJZJ_API_KEY.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
