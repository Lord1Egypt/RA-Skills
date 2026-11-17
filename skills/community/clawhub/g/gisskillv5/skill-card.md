## Description:

GIS_SKILL_V5.0 provides a comprehensive GIS knowledge and workflow system for coordinate systems, surveying and mapping standards, spatial data processing, GIS software operations, automation, quality inspection, and GeoEvolve feedback-driven maintenance.

This skill is for research and development only.

## Publisher:

[leo-gissss](https://clawhub.ai/user/leo-gissss)

### License/Terms of Use:

CC BY-NC-SA 4.0

## Use Case:

GIS practitioners, surveying teams, and geospatial developers use this skill to plan, validate, automate, and document GIS production workflows across coordinate transformation, GIS/CAD conversion, topology and quality checks, metadata generation, remote sensing, WebGIS, spatial databases, and standards compliance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad agent control and includes persistent self-updating behavior.

Mitigation: Review the workflow before installation and keep self-evolution, crawler, fixer, and index-rebuild scripts disabled unless they are explicitly needed and supervised.

Risk: Automated GIS processing can damage source data or produce incorrect outputs when run directly on operational datasets.

Mitigation: Use copies of GIS datasets, keep source data read-only, and review generated diffs, logs, and quality reports before applying changes.

Risk: Credential examples in the artifact may be insecure for production use.

Mitigation: Replace credential examples with HTTPS, least-privilege accounts, and header-only tokens before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leo-gissss/skills/gisskillv5)
- [V5 Constitution](V5_CONSTITUTION.md)
- [Version Matrix](VERSION_MATRIX.md)
- [Knowledge Base Overview](knowledge_base/README.md)
- [GeoEvolve Overview](geo_evolve/README.md)
- [GIS Knowledge Graph Overview](geo_kg/README.md)
- [Automation Scripts Overview](scripts/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code, shell commands, configuration snippets, checklists, reports, and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include generated GIS processing code, validation reports, logs, acceptance checklists, and human follow-up items for unresolved project parameters.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact package version 5.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
