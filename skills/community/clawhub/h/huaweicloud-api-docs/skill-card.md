## Description: <br>
Finds and summarizes official Huawei Cloud API documentation from Huawei Cloud Help Center and Huawei Cloud developer properties for service API references, developer guides, endpoints, authentication, SDKs, API Explorer, error codes, and service-specific documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevetdp](https://clawhub.ai/user/stevetdp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to locate, verify, and summarize official Huawei Cloud API documentation for cloud services such as OBS, ECS, VPC, RDS, CCE, ELB, IAM, and GaussDB. It supports documentation lookup, service identification, API Explorer navigation, and concise source-backed summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use web tools to search and open official Huawei Cloud documentation pages. <br>
Mitigation: Do not paste private credentials, tokens, account identifiers, or other sensitive data into prompts when using the skill. <br>
Risk: Documentation summaries can become incorrect if based on ambiguous service names, search snippets, unavailable pages, or outdated links. <br>
Mitigation: Prefer opened official Huawei Cloud pages, verify service matches by title or breadcrumb, and label unverified or inferred details clearly. <br>


## Reference(s): <br>
- [Huawei Cloud Help Center](https://support.huaweicloud.com/intl/en-us/index.html) <br>
- [Huawei Cloud Developer Center](https://developer.huaweicloud.com/eu/) <br>
- [Huawei Cloud Developer Tools](https://developer.huaweicloud.com/tool.html) <br>
- [Huawei Cloud API Explorer](https://console.huaweicloud.com/apiexplorer/) <br>
- [Huawei Cloud Console (International)](https://console-intl.huaweicloud.com/console/?locale=en-us) <br>
- [ClawHub Skill Page](https://clawhub.ai/stevetdp/huaweicloud-api-docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Official source links are included when web-enabled retrieval succeeds; when web tools are unavailable, the skill returns official entry links and states that service-specific documentation was not verified.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
