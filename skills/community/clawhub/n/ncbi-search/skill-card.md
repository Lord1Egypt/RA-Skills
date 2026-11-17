## Description:

Search NCBI databases using E-Utilities API (official, free). Supports 10+ databases: PubMed (literature), Gene, Protein, Nucleotide, dbSNP, ClinVar, Taxonomy, BioSample, Assembly, SRA. Automatically detects search intent and routes to appropriate database. Returns formatted results with key information. Use for biomedical literature, gene information, protein sequences, genetic variants, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[side-peng](https://clawhub.ai/user/side-peng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and biomedical analysts use this skill to guide an agent through NCBI E-Utilities searches across PubMed, Gene, Protein, Nucleotide, dbSNP, ClinVar, Taxonomy, BioSample, Assembly, and SRA. It helps choose the right NCBI database, construct searches, run the bundled scripts, and return readable summaries or JSON results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: NCBI API keys can be exposed in shell history or process listings when passed directly on the command line.

Mitigation: Set NCBI_API_KEY as an environment variable instead of passing the key as a command argument.

Risk: Biomedical queries and retrieved results can remain on disk through the local cache or explicit output-file options.

Mitigation: Disable caching with NCBI_NO_CACHE=1 for sensitive searches and manage output files according to the user's data-handling requirements.

Risk: The skill runs third-party Python scripts that make network requests to NCBI services.

Mitigation: Install and run the scripts in an isolated Python environment before using them in a shared or production workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/side-peng/skills/ncbi-search)
- [PubMed Query Syntax Guide](references/query_syntax.md)
- [NCBI E-Utilities API](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- [PubMed Help](https://pubmed.ncbi.nlm.nih.gov/help/)
- [MeSH Browser](https://mesh.nlm.nih.gov/)
- [PubMed Advanced Search Builder](https://pubmed.ncbi.nlm.nih.gov/advanced/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; command output can be summary text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write requested result files and may create a local SQLite cache unless caching is disabled.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
