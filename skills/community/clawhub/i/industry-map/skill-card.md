## Description:

Generates Chinese-language industry chain maps through deep research, first-level category discovery, and 5-7 layer hierarchy design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[memoryf](https://clawhub.ai/user/memoryf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to guide agents through industry research and create multi-level industry maps for industry-chain analysis, classification planning, and market-structure documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill calls for comprehensive web research and may be heavier than needed for simple market questions.

Mitigation: Confirm scope, language, and research depth before invoking it; use a lighter research pass for generic market questions.

Risk: Industry maps can reflect incomplete, outdated, or weakly supported sources, producing misleading classifications.

Mitigation: Require source-backed first-level categories and review the CSV and Markdown outputs before relying on them.

Risk: The skill writes CSV and Markdown outputs to a selected directory.

Mitigation: Confirm the output path before writing and avoid sensitive directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/memoryf/skills/industry-map)
- [Skill specification](artifact/SKILL.md)
- [Reference README](artifact/README.md)
- [Default CSV template](artifact/assets/default_template.csv)
- [Semiconductor industry map sample](artifact/半导体产业图谱.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, files]

**Output Format:** [CSV plus Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs normally include an 8-column industry-map CSV and, unless disabled, a Markdown process record with sources.]

## Skill Version(s):

1.0.0 (source: server release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
