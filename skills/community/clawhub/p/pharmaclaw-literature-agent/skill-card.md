## Description: <br>
Searches PubMed, Semantic Scholar, ClinicalTrials.gov, and bioRxiv/medRxiv for biomedical literature, trials, and preprints, returning structured paper and trial summaries with novelty-oriented ranking for drug-discovery workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cheminem](https://clawhub.ai/user/Cheminem) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and drug-discovery agents use this skill to mine public biomedical literature, clinical trial records, and preprints for compounds, targets, diseases, mechanisms, citations, and recent evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms may be sent to public research APIs, which can expose confidential compound names, proprietary targets, or unpublished research strategy terms. <br>
Mitigation: Avoid confidential or proprietary query terms and use only searches appropriate for public biomedical, preprint, and clinical-trial services. <br>
Risk: Literature, trial, and preprint summaries can be incomplete, outdated, or misleading if treated as medical or scientific conclusions. <br>
Mitigation: Verify important conclusions against the cited source papers, trial records, and domain expert review before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Cheminem/pharmaclaw-literature-agent) <br>
- [PubMed NCBI E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils) <br>
- [Semantic Scholar Graph API](https://api.semanticscholar.org/graph/v1) <br>
- [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/v2/studies) <br>
- [bioRxiv API](https://api.biorxiv.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON from helper scripts and Markdown or plain-text summaries from the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Public API queries are sent to external literature and clinical-trial services; no API keys are required.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
