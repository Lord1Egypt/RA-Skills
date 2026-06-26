## Description: <br>
Fetch articles from PubMed Central using NCBI APIs. Search journals, retrieve full text via OAI-PMH, batch harvest for RAG pipelines. No API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[angusthefuzz](https://clawhub.ai/user/angusthefuzz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and researchers use this skill to search PubMed Central, retrieve open-access article metadata, abstracts, or JATS XML full text, and batch harvest literature for review queues or RAG pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Literature searches and requested PMC IDs are sent to NCBI/PMC public APIs. <br>
Mitigation: Use the skill only when sending those queries and identifiers to NCBI/PMC is acceptable for the workflow. <br>
Risk: Large automated batches may hit NCBI rate limits or recommended usage windows. <br>
Mitigation: Respect the built-in request delay, keep batch sizes reasonable, and schedule large harvests outside NCBI peak hours where practical. <br>
Risk: No upstream source or homepage is listed in server-resolved provenance. <br>
Mitigation: Review future versions and their security evidence before automated or large-scale use. <br>


## Reference(s): <br>
- [PMC Harvest ClawHub release](https://clawhub.ai/angusthefuzz/pmc-harvest) <br>
- [NCBI E-utilities documentation](https://www.ncbi.nlm.nih.gov/books/NBK25501/) <br>
- [NCBI E-utilities endpoint](https://eutils.ncbi.nlm.nih.gov/entrez/eutils) <br>
- [PubMed Central OAI-PMH endpoint](https://pmc.ncbi.nlm.nih.gov/api/oai/v1/mh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell and JavaScript examples; runtime commands return console text and parsed article data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and network access to NCBI/PMC public APIs; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
