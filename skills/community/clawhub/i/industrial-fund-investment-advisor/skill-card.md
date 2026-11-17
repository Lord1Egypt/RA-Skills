## Description:

Provides Chinese-market industrial fund and private-market investment analysis using founder, industry, government, financial, industrial capability, comparison, sensitivity, and investment memo workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT

## Use Case:

Investment professionals and external users use this skill to analyze primary-market industrial investment opportunities, especially Chinese industrial funds, strategic investment, and government-guided fund scenarios. It supports deal screening, founder and sector assessment, government-fit analysis, financial return estimates, comparable-project review, sensitivity analysis, and investment memo generation.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Sensitive investment analysis may be written to local or global memory without clear consent or retention controls.

Mitigation: Disable or manually control memory writes for confidential deals, avoid sending non-public details to search or Tencent Docs, and review or delete memory files after use.

Risk: Investment conclusions may rely on public data gaps or estimates where private-company financials are unavailable.

Mitigation: Require source attribution, mark estimates explicitly, review confidence scores, and route final investment decisions to a human investment committee.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/perrykono-debug/skills/industrial-fund-investment-advisor)
- [SKILL.md](artifact/SKILL.md)
- [Investment analyst workspace](artifact/references/agents.md)
- [Industrial investment analyst identity](artifact/references/identity.md)
- [Investment analyst tools](artifact/references/tools.md)
- [Industrial investment analyst architecture](artifact/references/soul.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown investment memos, structured scoring tables, JSON-like analysis blocks, and optional exported report content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs distinguish sourced facts from estimates, include confidence scoring, and may trigger docx, PDF, or Tencent Docs export workflows when requested.]

## Skill Version(s):

1.2.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
