## Description:

My PubMed Search helps agents search PubMed literature through web search or the NCBI E-Utilities API and format results with citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hollyya](https://clawhub.ai/user/hollyya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use this skill to search PubMed, retrieve article metadata and abstracts, and format citations for medical literature review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to NCBI/PubMed.

Mitigation: Avoid sensitive patient or confidential data in search terms and review external service expectations before use.

Risk: The artifact documentation references PowerShell scripts that are not included, while the included implementation is Python.

Mitigation: Review and adjust command examples before deployment, using the included Python script or adding the missing scripts deliberately.

Risk: Literature search results can be incomplete, stale, or require professional interpretation.

Mitigation: Verify important results against PubMed or source publications and apply appropriate domain review before relying on findings.

## Reference(s):

- [PubMed API usage guide](references/pubmed-api.md)
- [NCBI E-Utilities API](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/)
- [PubMed API](https://www.ncbi.nlm.nih.gov/research/pubmed-api/)
- [ClawHub skill page](https://clawhub.ai/hollyya/skills/my-pubmed-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with result tables, citation entries, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return PubMed article metadata, abstracts, PMIDs, DOIs, and citations in APA, MLA, IEEE, GB/T 7714, or BibTeX style.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
