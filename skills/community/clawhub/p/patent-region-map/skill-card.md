## Description:

按技术方向统计专利在省、市或国家间的地域分布，并汇总各地主要专利申请单位。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:


## Use Case:

研究人员、产业分析师和招商团队可按指定技术主题了解专利在中国省市或全球国家间的分布，并识别各地主要申请单位。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential routing weaknesses could expose a paid API key.

Mitigation: Request fixes before supplying a paid key; keep keys out of chat and shared plaintext files, and use a restricted key with a spending limit.

Risk: File-cache containment weaknesses warrant review before installation.

Mitigation: Request cache-containment fixes and review the behavior before installation or use with sensitive data.

Risk: Unexpectedly empty regional statistics could lead to misleading conclusions.

Mitigation: Cross-check unexpectedly empty regional statistics before reporting results.

Risk: Research details sent to the external service may include information the user has not authorized for sharing.

Mitigation: Send only research details the user authorizes PatentMax to receive.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ip930/skills/patent-region-map)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)

## Skill Output:

**Output Type(s):** [Analysis, Tables, CSV files]

**Output Format:** [Concise regional analysis and UTF-8 CSV tables compatible with Excel]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Regional counts, leading organizations, and recent trends; CSV uses a UTF-8 BOM for spreadsheet compatibility.]

## Skill Version(s):

1.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
