## Description:

Analyze one competitor's patent portfolio architecture in a defined technology, including public technical context, entity-resolved patent retrieval, representative-family selection, claim and specification review, core-versus-peripheral protection hypotheses, technical-density mapping, product-feature visualization, geographic filing behavior, and evidence-backed R&D actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Corporate IP teams, R&D engineers, product leaders, and strategy analysts use this skill to monitor one competitor's patent activity in a defined technology area and produce evidence-backed patent landscape reports. It supports strategy and research prioritization, not infringement, validity, or freedom-to-operate conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent search inputs, retrieved patent data, and generated reports may include confidential business strategy or sensitive research context.

Mitigation: Use the skill only in an approved PatSnap and agent environment, and avoid supplying confidential data unless that environment is authorized for it.

Risk: PatSnap API keys or MCP credentials could be exposed if copied into prompts, reports, logs, or saved analysis files.

Mitigation: Keep API keys secret, use configured MCP credentials rather than embedding secrets in artifacts, and review outputs before sharing them.

Risk: A patent landscape report could be mistaken for legal clearance, infringement analysis, validity analysis, or freedom-to-operate advice.

Mitigation: Treat outputs as strategy research, preserve the non-legal-opinion boundary, and route clearance or legal conclusions to qualified IP counsel.

## Reference(s):

- [Competitor patent landscape workflow guide](references/workflow_guide.md)
- [PatSnap Advanced Patent Search MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [PatSnap Patent Briefing MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)
- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/monitor-competitor-patent-landscape-ip)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown workflow guidance, JSON analysis contract, shell commands, and generated HTML or PDF report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are based on declared scope, PatSnap patent retrieval, verified patent identifiers, stated counting units, and explicit limitations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
