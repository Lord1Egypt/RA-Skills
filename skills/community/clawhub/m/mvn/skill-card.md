## Description:

Maven MCP Server是一个通过自然语言交互的AI驱动Maven依赖管理工具，提供版本检查、安全扫描和依赖分析功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check Maven dependency versions, list available artifact versions, scan Java Maven projects for vulnerabilities, and analyze individual POM files through a remote Maven analysis service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores an API key in a local .env file and can send Maven coordinates, workspace paths, POM paths, profiles, and scan parameters to an overridable remote API endpoint.

Mitigation: Use it only in trusted workspaces, avoid long-lived shared API keys, review the configured endpoint before use, and rotate the key if it may have been committed or shared.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/mvn)
- [alinklab publisher profile](https://clawhub.ai/user/alinklab)
- [XiaoBenYang API key site](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API Calls, guidance]

**Output Format:** [Markdown summaries of JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY credential before remote Maven analysis tools can be used.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
