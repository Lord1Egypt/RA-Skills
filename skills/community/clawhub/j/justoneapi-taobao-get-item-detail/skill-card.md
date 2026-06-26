## Description: <br>
Call 5 get-item-detail versions for Taobao and Tmall Product Details through JustOneAPI with itemId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ecommerce analysts use this skill to retrieve Taobao and Tmall product detail data, including pricing, images, and shop information, from JustOneAPI by item ID. It supports product research, catalog monitoring, and ecommerce analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent as a URL query parameter and could be exposed through logs, shared command lines, screenshots, or request traces. <br>
Mitigation: Use a scoped or low-privilege token where possible, avoid sharing full request URLs or command output that includes credentials, and rotate the token if exposure is suspected. <br>
Risk: The skill calls a third-party API service and depends on JustOneAPI availability, authorization, and response behavior. <br>
Mitigation: Install only when the publisher and service are trusted, keep the token in the required environment variable, and surface backend status and payload details when requests fail. <br>
Risk: The v2 product-detail flow can return a pending task status instead of completed product data. <br>
Mitigation: Report the operation ID, endpoint path, and pending status clearly so the user can retry or choose another supported version. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-taobao-get-item-detail) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao_get_item_detail&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token and an itemId; the v2 operation may return a pending task status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
