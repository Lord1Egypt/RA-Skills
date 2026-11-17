## Description:

Build ORBCAFE graph analytics dialogs, detail pages, and AI settings flows using CGraphReport, chart components, CDetailInfoPage/useDetailInfo, and CCustomizeAgent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenruiyang](https://clawhub.ai/user/shenruiyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement ORBCAFE graph report dialogs, searchable detail pages with AI fallback, and configurable LLM prompt settings flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI settings examples include API key fields that could be mishandled by an application.

Mitigation: Keep API key storage and logging in application configuration and avoid exposing keys in logs or client-visible debug panels.

Risk: Generated ORBCAFE snippets could omit required component state or props.

Mitigation: Check the chosen recipe and guardrails before use, including required props for CGraphReport, CDetailInfoPage, and CCustomizeAgent.

## Reference(s):

- [Domain Selector](artifact/references/domain-selector.md)
- [Graph + Detail + Agent Guardrails](artifact/references/guardrails.md)
- [Graph + Detail + Agent Recipes](artifact/references/recipes.md)
- [ClawHub Skill Page](https://clawhub.ai/shenruiyang/skills/orbcafe-graph-detail-ai)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with focused TSX snippets and data model guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a chosen module, minimal code, data model shape, and one suggested extension.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
