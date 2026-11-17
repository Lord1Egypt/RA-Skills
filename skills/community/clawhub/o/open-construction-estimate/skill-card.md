## Description:

Access and utilize open construction pricing databases. Match BIM elements to standardized work items, calculate costs using public unit price databases with 55,000+ work items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and construction estimators use this skill to match element descriptions or BIM data to standardized construction work items, apply regional cost factors, and calculate cost estimates from open pricing databases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exported estimates, pricing CSVs, and modified pricing databases may contain sensitive business records.

Mitigation: Choose output paths and data sources deliberately, restrict sharing of generated files, and review estimate exports before distribution.

Risk: The skill may read local pricing data and access pricing-related network endpoints.

Mitigation: Install only in environments where the disclosed file and network access are acceptable, and use trusted pricing data sources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/datadrivenconstruction/skills/open-construction-estimate)
- [CSI MasterFormat](https://www.csiresources.org/standards/masterformat)
- [DataDrivenConstruction Website](https://datadrivenconstruction.io)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [Markdown responses with tabular estimates, JSON-like records, Python code snippets, and optional Excel or CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confidence scores, CSI division summaries, regional cost adjustments, and manual-review flags for missing or low-confidence matches.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact/claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
