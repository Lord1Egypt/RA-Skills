## Description:

Fetch articles from PubMed Central using NCBI APIs. Search journals, retrieve full text via OAI-PMH, batch harvest for RAG pipelines. No API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[angusthefuzz](https://clawhub.ai/user/angusthefuzz)

### License/Terms of Use:


## Use Case:

Developers and researchers use this skill to search PubMed Central, retrieve open-access article XML or abstracts, and batch-harvest article metadata for review queues or RAG pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes broader network access than its PubMed Central harvesting purpose documents.

Mitigation: Review before installing in environments with sensitive internal network access; prefer a version restricted to eutils.ncbi.nlm.nih.gov and pmc.ncbi.nlm.nih.gov with request timeouts and response-size limits.

Risk: Large batch harvests can exceed public NCBI usage expectations or run during discouraged peak hours.

Mitigation: Keep rate limiting enabled, use conservative batch sizes, and schedule large runs outside NCBI's documented peak-hour window.

## Reference(s):

- [PMC Harvest on ClawHub](https://clawhub.ai/angusthefuzz/skills/pmc-harvest)
- [NCBI E-utilities API](https://eutils.ncbi.nlm.nih.gov/entrez/eutils)
- [PubMed Central OAI-PMH API](https://pmc.ncbi.nlm.nih.gov/api/oai/v1/mh)
- [NCBI E-utilities Documentation](https://www.ncbi.nlm.nih.gov/books/NBK25501/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JavaScript code blocks; CLI output may include article metadata, abstracts, and XML-derived text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Node.js and public NCBI APIs without an API key; requests are rate-limited in the artifact.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
