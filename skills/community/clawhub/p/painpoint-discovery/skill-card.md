## Description:

Painpoint discovery expert. Helps users discover, analyze, and evaluate startup painpoints in specific domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyuxing](https://clawhub.ai/user/lyuxing)

### License/Terms of Use:


## Use Case:

Entrepreneurs, product managers, investors, and developers use this skill to research a domain, identify recurring user complaints, structure painpoints, and assess startup opportunities with suggested solution directions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Domain keywords and related browsing activity may be sent to search engines and public websites during research.

Mitigation: Avoid entering sensitive, confidential, or regulated business information as search terms; review planned searches before deep research.

Risk: Research output can include incomplete or misleading market, competition, or willingness-to-pay conclusions.

Mitigation: Treat reports as discovery inputs, require source citations, and validate priority painpoints with interviews or other real-world evidence before product decisions.

Risk: Deep-research mode can take about 30 minutes and create local Markdown report files.

Mitigation: Choose quick mode for exploratory work, reserve deep mode for saveable reports, and review generated files before sharing or committing them.

Risk: Reports in health, finance, legal, or similarly regulated domains may surface recommendations that need domain-specific compliance review.

Mitigation: Add appropriate disclaimers and have qualified reviewers check regulated-domain outputs before using them externally.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lyuxing/skills/painpoint-discovery)
- [Skill Definition](artifact/SKILL.md)
- [Painpoint Discovery README](artifact/README.md)
- [Runner Workflow](artifact/runner.md)
- [Standalone Agent Configuration](artifact/agent-config.md)
- [Example Report](artifact/example-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown research reports with structured painpoint analysis, recommendations, and optional Mermaid knowledge graph code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deep-research mode may create local Markdown report files under painpoint-reports/.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
