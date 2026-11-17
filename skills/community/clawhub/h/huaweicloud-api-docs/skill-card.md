## Description:

Find and summarize official Huawei Cloud API documentation from Huawei Cloud Help Center and Huawei Cloud developer properties for service APIs, references, guides, endpoints, authentication, SDKs, API Explorer, and error codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevetdp](https://clawhub.ai/user/stevetdp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to locate, verify, and summarize official Huawei Cloud API documentation for a named service. It supports documentation lookup for API references, developer guides, authentication, endpoints, SDKs, API Explorer, and error codes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may provide limited guidance when official Huawei Cloud pages cannot be searched or opened in the current agent environment.

Mitigation: Disclose the retrieval limitation and provide official Huawei Cloud entry links instead of guessing service-specific API details.

Risk: Ambiguous service abbreviations can point to multiple Huawei Cloud products.

Mitigation: List likely candidate services, ask the user to choose, and identify the normalized service name used for retrieval.

## Reference(s):

- [Huawei Cloud Help Center](https://support.huaweicloud.com/intl/en-us/index.html)
- [Huawei Cloud Developer Center](https://developer.huaweicloud.com/eu/)
- [Huawei Cloud Developer Tools](https://developer.huaweicloud.com/tool.html)
- [Huawei Cloud API Explorer](https://console.huaweicloud.com/apiexplorer/)
- [Huawei Cloud Console International](https://console-intl.huaweicloud.com/console/?locale=en-us)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with official source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include verified official Huawei Cloud links or no-web fallback entry links, depending on available retrieval tools.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
