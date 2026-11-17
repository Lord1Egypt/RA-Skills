## Description:

Build ORBCAFE standard report/list pages with CStandardPage, CTable, CSmartFilter, useStandardReport, persistence, and quickCreate/quickEdit/quickDelete using official examples-proven patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenruiyang](https://clawhub.ai/user/shenruiyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement ORBCAFE report and list pages with standard filters, tables, pagination, persistence, quick operations, and verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated setup guidance may ask the agent to install npm packages before building ORBCAFE report pages.

Mitigation: Review package installation commands against the target project before running them.

Risk: Generated quickCreate, quickEdit, or quickDelete callbacks may affect production data if connected without review.

Mitigation: Review callback payloads and data writes before connecting them to real production services.

Risk: Locale or pagination assumptions may not match the target application or backend API.

Mitigation: Set locale through ORBCAFE's supported providers and map ALL pagination requests explicitly when the backend does not accept limit = -1.

## Reference(s):

- [StdReport Component Selection](references/component-selection.md)
- [StdReport Guardrails](references/guardrails.md)
- [StdReport Recipes](references/recipes.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript/TSX and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes mode selection, paste-ready ORBCAFE imports, data-contract notes, verification steps, and troubleshooting guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
