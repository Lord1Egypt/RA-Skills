## Description:

为携程酒店、民宿商家执行经营体检、点评分流与回复、价格房态和订单提案、竞品分析及笔记内容生产，读取真实门店数据或用户导出，生成离线 HTML 报告，并通过独立 Chrome 和经实测的账户适配执行已授权动作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlxcn](https://clawhub.ai/user/openlxcn)

### License/Terms of Use:

MIT-0

## Use Case:

Hotel, inn, and homestay operators use this skill to turn Ctrip merchant data or user exports into an offline operations report, review-response proposals, pricing and inventory proposals, competitor analysis, and content drafts. Authorized account actions should be used only after account mapping, policy hashes, object identity, and readback checks are in place.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can support high-impact hotel account automation, including price, inventory, order, review, and content workflows.

Mitigation: Enable automatic actions only after checking the exact policy, content hash, account mapping, object identity, authorization, and rollback or readback plan.

Risk: The hotel workspace may contain reports, evidence captures, action logs, browser session state, license data, and business information.

Mitigation: Keep the workspace private, use a dedicated hotel workspace and isolated Chrome session, and avoid placing workspace data in public repositories.

Risk: Some real Ctrip merchant-account mappings, write actions, and public content readbacks were not yet live-verified for this release.

Mitigation: Treat affected outputs as proposals or drafts until live account evidence exists; stop unmapped actions and rely on per-object readback before recording success.

## Reference(s):

- [Runtime and Account Adaptation](references/runtime.md)
- [Version Status](references/status.json)
- [Capability Matrix](references/capability-matrix.json)
- [Product Catalog](references/catalog.json)
- [GitHub release v0.1.1](https://github.com/openlxcn/openlx-ctrip-hotel-ops/releases/tag/v0.1.1)
- [Public product status](https://ctrip.openlx.cn/status.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, local HTML reports, JSON configuration, and action proposal records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local workspace state and evidence records; reports and proposals should preserve source, authorization, action, and readback status.]

## Skill Version(s):

0.1.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
