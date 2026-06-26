## Description: <br>
Searches PubMed literature using web search and the NCBI E-Utilities API, with support for filters, article details, and citation formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hollyya](https://clawhub.ai/user/hollyya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, clinicians, students, and developers use this skill to search PubMed, inspect article metadata and abstracts, and format citations for literature review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PubMed queries may contain private health details, secrets, or unrelated sensitive information and are sent to NCBI. <br>
Mitigation: Avoid entering private health details, secrets, or unrelated sensitive data in search queries. <br>
Risk: The documentation names PowerShell scripts that are not present in this version. <br>
Mitigation: Use the packaged Python script at scripts/pubmed_search.py or verify script names before execution. <br>
Risk: Search results, abstracts, and generated citations may be incomplete or need domain review. <br>
Mitigation: Verify important papers, metadata, and citations against PubMed or the original publication before relying on them. <br>


## Reference(s): <br>
- [PubMed API usage guide](references/pubmed-api.md) <br>
- [NCBI E-Utilities API](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/) <br>
- [NCBI PubMed API](https://www.ncbi.nlm.nih.gov/research/pubmed-api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown tables, formatted citations, Python script output, and usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports PubMed IDs, article metadata, abstracts, DOI fields, and APA, MLA, IEEE, GB/T 7714, and BibTeX-style citation workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
