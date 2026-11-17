## Description:

对企业或组织进行合规的外贸客户开发与决策人信息查询。仅在用户明确授权、且符合当地隐私、反垃圾和商业通信法规的前提下使用；可按企业名称、企业网址域名或 LinkedIn 企业号查询企业基本信息与决策人联系方式，并在必要时提供有限的联系人线索。禁止用于未经授权的个人信息收集、骚扰式营销、隐私侵害或其他违法违规场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[oraagent](https://clawhub.ai/user/oraagent)

### License/Terms of Use:

MIT-0

## Use Case:

Business development, sales, and trade research users can query authorized company, domain, or LinkedIn company inputs to retrieve company details and limited decision-maker contact leads. The skill is intended only for compliant, authorized lookups under applicable privacy, anti-spam, and commercial communication rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends company and contact lookup inputs to an external Topeasy API.

Mitigation: Use it only for authorized searches where the user accepts the external data processing.

Risk: Raw company and contact results are written to a predictable shared temp directory.

Mitigation: Delete or protect generated files after use, especially on shared machines.

Risk: The skill reads a local OraAgent.key for API authorization.

Mitigation: Install and run it only where that key is expected, protected, and permitted for the lookup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oraagent/skills/ora-contact-pro)
- [OraAgent publisher profile](https://clawhub.ai/user/oraagent)
- [Topeasy API endpoint](https://api.topeasychina.com:6443/TPAiAgentSkill)
- [OraAgent platform](https://www.oraskl.com/platform)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown summary with shell command execution and JSON result file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries may create raw JSON result files under the ora-contact-pro temp directory.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
