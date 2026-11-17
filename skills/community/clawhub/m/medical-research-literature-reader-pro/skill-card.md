## Description:

Medical Research Literature Reader Pro helps clinical, bioinformatics, translational, and experimental researchers analyze medical and scientific papers with evidence-type routing, critical appraisal, interpretation-boundary checks, and follow-up research generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, clinicians, bioinformaticians, and lab teams use this skill to read, critique, and interpret medical or scientific papers from PDFs, abstracts, titles, DOIs, PMIDs, figures, or citation strings. It produces track-specific analysis for clinical, computational, experimental, and hybrid papers, with optional downstream deliverables for journal clubs, comparison, replication planning, PI decisions, and follow-up study design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may provide confidential unpublished research, patient-identifying clinical information, or restricted PDFs for analysis.

Mitigation: Use only in an agent environment approved for that material, de-identify sensitive inputs when possible, and avoid submitting restricted documents unless processing is permitted.

Risk: Generated related-study or citation suggestions may be incomplete or incorrect when the agent lacks reliable literature access.

Mitigation: Verify publication details, citations, PMIDs, and related-study lists against trusted literature databases before relying on or citing them.

Risk: Paper analysis may be incomplete when only a title, abstract, DOI, PMID, figure, or partial text is available.

Mitigation: State what input was available, mark sections that require full text, and request the abstract, methods, results, figures, or supplementary material needed for full appraisal.

Risk: Research outputs can overstate causal, mechanistic, translational, or clinical readiness claims if the source paper itself overclaims.

Mitigation: Use evidence-type-specific language, distinguish association from causation and prediction from mechanism, and explicitly identify interpretation boundaries in the report.

## Reference(s):

- [Track Analysis Modules](references/tracks.md)
- [Expert Deep Review Extensions](references/expert_review_extensions.md)
- [Similar Literature Module](references/literature_module.md)
- [Follow-Up Questions Module](references/followup_module.md)
- [Plugin System](references/plugins.md)
- [Reporting Style and Interpretation Safety](references/reporting_style.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown structured reports, tables, briefs, question lists, and research workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mode-specific outputs may include quick reads, structured reports, expert reviews, journal club kits, comparison tables, PI briefs, replication starters, mind maps, and follow-up experiment designs.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
