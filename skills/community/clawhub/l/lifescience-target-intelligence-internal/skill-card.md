## Description:

Supports internal target-level competitive intelligence for biological drug targets, including pipeline, clinical, patent, validation, and strategic analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fubian-ai](https://clawhub.ai/user/fubian-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Life-sciences analysts and R&D, BD, or investment teams use this router-invoked skill to assess biological targets, map competitors, review clinical and patent evidence, and produce GO/NO-GO recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External lookups to public scientific databases and web search can disclose target names, gene IDs, and commercial research questions.

Mitigation: Confirm those disclosures are acceptable for the research context before installation or use, and minimize query detail where confidentiality matters.

Risk: Target intelligence reports may rely on time-sensitive public and MCP-backed evidence that can be incomplete or stale.

Mitigation: Require source attribution, note data currency, preserve evidence gaps, and avoid forcing conclusions when evidence is insufficient.

## Reference(s):

- [Detailed Search Examples](references/detailed-search-examples.md)
- [Report Templates](references/report-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/fubian-ai/skills/lifescience-target-intelligence-internal)
- [Patsnap Pharma Intelligence MCP Server](https://open.patsnap.com/marketplace/mcp-servers/245f3ce8-79e4-4c2a-927c-e155c293f097)
- [UniProt REST API](https://rest.uniprot.org/uniprotkb/{uniprot_id}.json)
- [STRING Network API](https://string-db.org/api/json/network)
- [BioGRID Interactions API](https://webservice.thebiogrid.org/interactions)
- [ChEMBL Activity API](https://www.ebi.ac.uk/chembl/api/data/activity.json)
- [Open Targets Platform API](https://api.platform.opentargets.org/api/v4/graphql)
- [RCSB PDB Data API](https://data.rcsb.org/rest/v1/core/entry/[pdb_id])
- [PDBe Validation API](https://www.ebi.ac.uk/pdbe/api/validation/residuewise_outlier_summary/entry/{pdb_id})
- [DisGeNET Gene-Disease API](https://www.disgenet.org/api/gda/gene/[gene_id])
- [GenCC Gene Search](https://search.thegencc.org/genes/[hgnc_id])

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown reports with tables, inline references, and optional Mermaid or SVG visual artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include separated Tier P primary competitive data and Tier S curated scientific evidence sections.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
