## Description:

Searches and retrieves biomedical literature, clinical trial records, and preprints from public research services with structured summaries, citation tracking, novelty scoring, and open-access links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheminem](https://clawhub.ai/user/cheminem)

### License/Terms of Use:


## Use Case:

Researchers, drug discovery teams, and agent workflows use this skill to search publications, preprints, and late-phase clinical trials for compounds, targets, diseases, mechanisms, reactions, and catalysts. It supports DOI/PMID lookup, citation and related-paper discovery, and follow-on recommendations for pharmaceutical analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Literature queries and paper identifiers are sent to public third-party research services.

Mitigation: Do not use proprietary, unpublished, patient-specific, or confidential research terms unless that disclosure is acceptable in the deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cheminem/skills/pharmaclaw-literature-agent)
- [PubMed E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils)
- [Semantic Scholar Graph API](https://api.semanticscholar.org/graph/v1)
- [ClinicalTrials.gov API](https://clinicaltrials.gov/data-api/v2/studies)
- [bioRxiv API](https://api.biorxiv.org)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and structured JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries and paper identifiers may be sent to public third-party research services.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
