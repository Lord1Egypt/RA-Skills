## Description: <br>
Searches NCBI databases through the official E-Utilities API and routes biomedical literature, gene, protein, nucleotide, dbSNP, ClinVar, taxonomy, BioSample, Assembly, and SRA queries to the appropriate database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[side-peng](https://clawhub.ai/user/side-peng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to run NCBI and PubMed searches, route biomedical queries to the right database, fetch summaries or JSON results, and batch fetch PubMed article details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Biomedical search terms are sent to NCBI. <br>
Mitigation: Avoid sensitive queries when that disclosure is inappropriate, or confirm that sending the query to NCBI is acceptable before use. <br>
Risk: Returned NCBI results may be stored locally in the SQLite cache. <br>
Mitigation: Set NCBI_NO_CACHE=1 for sensitive searches or clear .ncbi_cache/cache.db after use on shared machines. <br>
Risk: Passing an NCBI API key on the command line can expose it through shell history or process listings. <br>
Mitigation: Prefer the NCBI_API_KEY environment variable instead of the --api-key argument. <br>


## Reference(s): <br>
- [PubMed Query Syntax Guide](references/query_syntax.md) <br>
- [NCBI E-Utilities Documentation](https://www.ncbi.nlm.nih.gov/books/NBK25501/) <br>
- [NCBI Database List](https://www.ncbi.nlm.nih.gov/books/NBK25500/table/chapter.T5/) <br>
- [PubMed Help](https://pubmed.ncbi.nlm.nih.gov/help/) <br>
- [ClawHub Skill Page](https://clawhub.ai/side-peng/ncbi-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with bash commands; command output can be summary text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save results to files when requested; repeated NCBI API responses may be stored in a local SQLite cache.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
