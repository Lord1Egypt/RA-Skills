## Description:

Search, download, convert, organize, and audit academic literature collections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isonaei](https://clawhub.ai/user/isonaei)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to build and maintain academic literature collections by finding papers, downloading PDFs, converting them to markdown, organizing reference folders, collecting related resources, and auditing collection consistency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a Sci-Hub paywall-bypass path that can create legal, terms-of-service, or policy exposure.

Mitigation: Prefer open-access and publisher sources, and avoid the Sci-Hub path unless the user has confirmed the legal right and policy approval for that use.

Risk: Helper scripts perform network downloads and write files based on user-supplied inputs.

Mitigation: Run the scripts in a restricted working directory without sensitive files or credentials, and review DOI, URL, filename, and reference-directory inputs before execution.

Risk: The PDF conversion fallback can fetch runtime packages through uvx.

Mitigation: Pin or preinstall conversion dependencies in a managed environment before use.

## Reference(s):

- [Google Scholar search](https://scholar.google.com/scholar?q=QUERY&as_ylo=YEAR)
- [NCBI E-utilities PMC DOI lookup](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term=${DOI}&retmode=xml)
- [arXiv API DOI search](http://export.arxiv.org/api/query?search_query=doi:${DOI}&max_results=1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update PDF, markdown, README, RESOURCES, index.json, and resources.json files in a user-provided references directory.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
