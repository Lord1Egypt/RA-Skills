## Description:

pps-tag supports patent panorama tagging by recommending a four-column technology taxonomy, key technical questions, representative patent packages, demo tagging samples, and SaaS-ready candidate exports without performing full-sample tagging itself.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent analysts and agent workflows use this skill after candidate-pool tagging and panorama statistics are available to design a patent taxonomy, select representative patent packages, prepare demo tagging records, and export candidate records for downstream SaaS tagging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow has phase-boundary ambiguity because it requires tagged_pool.csv while also producing to_be_tagged.csv for later SaaS tagging.

Mitigation: Confirm the intended handoff before use, document which tagging step has already happened, and align required inputs and exports with that decision.

Risk: The skill depends on PatSnap MCP/API access for patent data retrieval and analysis.

Mitigation: Verify PatSnap account authorization and MCP connectivity before running the workflow, and fall back to framework-only guidance if access is unavailable.

Risk: Patent taxonomy and package outputs can be misleading if prerequisite inputs are stale, incomplete, or missing.

Mitigation: Require candidate_pool.csv, tech_taxonomy.txt, tagged_pool.csv, panorama_stats.json, and value_signals.json before producing final taxonomy, package, or tagging-export artifacts.

## Reference(s):

- [Query and Taxonomy Methodology](artifact/references/query-and-taxonomy-methodology.md)
- [PatSnap Open Platform](https://open.zhihuiya.com/)
- [PatSnap API Authentication Guide](https://open.zhihuiya.com/devportal/guides/authentication)
- [PatSnap MCP Server Marketplace](https://open.zhihuiya.com/marketplace/mcp-servers)
- [PatSnap Developer Portal](https://open.patsnap.com/devportal)

## Skill Output:

**Output Type(s):** [JSON, CSV, Markdown, HTML, Guidance, Configuration]

**Output Format:** [Structured files: JSON taxonomy and questions, CSV patent packages and tagging exports, Markdown proposal, and optional HTML report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written as project artifacts for patent panorama workflows and depend on prior candidate-pool, taxonomy, tagging, statistics, and value-signal inputs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
