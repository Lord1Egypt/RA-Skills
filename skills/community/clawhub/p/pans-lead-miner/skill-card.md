## Description:

Pans Lead Miner mines AI compute sales leads by searching a local SearXNG service across public funding, GitHub, LinkedIn, and news sources, then ranking prospects by funding stage and compute-demand signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashiming](https://clawhub.ai/user/dashiming)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and sales operators use this skill to discover and prioritize companies with public signals of AI compute demand from funding, project, LinkedIn, and news search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search results and snippets are untrusted web content and may be inaccurate or misleading.

Mitigation: Review URLs and snippets before outreach or business decisions, and do not treat the heuristic signal score as verified demand.

Risk: The tool can fall back to demo leads when SearXNG is unavailable, which may make sample records appear in normal output.

Mitigation: Check source and demo indicators before using results, and rerun against a working local SearXNG service for real prospecting.

Risk: Exported Markdown, JSON, or CSV lead files may persist locally and contain prospect data.

Mitigation: Choose export paths deliberately and handle generated files according to local data-retention and access policies.

## Reference(s):

- [Pans Lead Miner on ClawHub](https://clawhub.ai/dashiming/skills/pans-lead-miner)
- [dashiming publisher profile](https://clawhub.ai/user/dashiming)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, CSV, files]

**Output Format:** [Markdown table by default, JSON or CSV on request, optionally exported to a local file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are ranked by heuristic signal score and may come from local SearXNG search or demo fallback data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
