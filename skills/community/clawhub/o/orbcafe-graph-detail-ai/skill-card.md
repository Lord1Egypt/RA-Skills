## Description: <br>
Build ORBCAFE graph analytics dialogs, detail pages, and AI settings flows using CGraphReport, chart components, CDetailInfoPage/useDetailInfo, and CCustomizeAgent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SHENRUIYANG](https://clawhub.ai/user/SHENRUIYANG) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to implement ORBCAFE graph drilldowns, searchable detail tabs, and configurable AI prompt settings with the expected ORBCAFE UI components and data shapes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider keys and LLM API settings can be exposed through logs, hardcoded UI values, or client-visible debug panels. <br>
Mitigation: Keep provider keys in secure application configuration, avoid hardcoding or logging secrets, and limit client-visible settings to non-sensitive values. <br>
Risk: AI settings and prompt templates can change application behavior when edited by unauthorized users. <br>
Mitigation: Restrict who can edit or save LLM settings and prompt templates, and persist settings plus selected template IDs together. <br>
Risk: Generated graph or detail snippets may be incorrect if required ORBCAFE props or filter wiring are omitted. <br>
Mitigation: Review generated snippets against the required component props and only enable interactive filtering when filter state wiring is present. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SHENRUIYANG/orbcafe-graph-detail-ai) <br>
- [Domain Selector](references/domain-selector.md) <br>
- [Graph + Detail + Agent Guardrails](references/guardrails.md) <br>
- [Graph + Detail + Agent Recipes](references/recipes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with focused TypeScript/TSX snippets and data model guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes the chosen module, minimal code, required data model shape, and one extension recommendation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
