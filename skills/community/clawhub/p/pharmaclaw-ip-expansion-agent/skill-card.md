## Description:

Pharmaclaw Ip Expansion Agent helps pharma drug discovery and development teams analyze molecules and patent context for portfolio tracking, infringement and FTO review, prior art novelty suggestions, and strategic claim recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheminem](https://clawhub.ai/user/cheminem)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to support pharma IP portfolio analysis, patent/FTO triage, prior art review, and patentable molecule-derivative ideation from SMILES, keywords, or related agent outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive molecule, patent, or strategy data may be sent to external patent and compound services.

Mitigation: Use only data approved for disclosure to PatentsView and PubChem, and require explicit approval before any network lookup.

Risk: Reports, database entries, visualizations, and logs may persist pharma IP analysis results locally.

Mitigation: Run in an isolated environment, review output locations before execution, and require approval before report writes, database updates, logging, or scheduled portfolio checks.

Risk: Unpinned or unverified dependencies can introduce environment and supply-chain risk.

Mitigation: Pin and verify dependencies in a controlled Python environment before installing or running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cheminem/skills/pharmaclaw-ip-expansion-agent)
- [Patent/Compound APIs](references/apis.md)
- [USPTO API Catalog](https://developer.uspto.gov/api-catalog)
- [EPO Open Patent Services](https://developers.epo.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [JSON and Markdown reports with optional PNG or SVG visualization files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include risk findings, novelty suggestions, portfolio results, recommendations, and visualization paths.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
