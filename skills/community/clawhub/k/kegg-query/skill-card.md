## Description:

KEGG Query helps agents query KEGG for drug information, pathway analysis, and disease-drug-target discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hollyya](https://clawhub.ai/user/hollyya)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and biomedical researchers use this skill to look up KEGG drugs, analyze pathways, and discover disease-associated drugs, genes, and therapeutic targets for bioinformatics workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public KEGG REST API requests may expose submitted query terms and depend on external service availability.

Mitigation: Use appropriate non-sensitive KEGG identifiers or query terms, and confirm that public KEGG requests are acceptable for the workflow.

Risk: Example request code may run without production-grade request timeouts.

Mitigation: Add explicit request timeouts and retry or backoff behavior before production use.

Risk: Some curl examples redirect API output to local files.

Mitigation: Choose explicit, non-conflicting filenames before running commands that write downloaded KEGG outputs.

## Reference(s):

- [KEGG API Documentation](https://www.kegg.jp/kegg/rest/keggapi.html)
- [KEGG API Operations Reference](artifact/references/kegg_api_operations.md)
- [KEGG Databases Reference](artifact/references/kegg_databases.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with Python code examples, shell commands, and structured JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include KEGG identifiers, drug details, pathway genes and compounds, disease associations, and API troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
