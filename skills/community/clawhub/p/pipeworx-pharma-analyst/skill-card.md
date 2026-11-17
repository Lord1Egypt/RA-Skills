## Description:

Access integrated clinical trial, FDA drug, and RxNorm data for pharmaceutical research analysis, including drug profiles, pipeline scans, safety reports, and trial lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to Pipeworx's pharmaceutical research MCP gateway for drug, clinical trial, safety, approval, label, recall, and RxNorm-oriented analysis. It is intended to help gather and compare public pharmaceutical data, with medical and regulatory conclusions verified against authoritative sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pharmaceutical research queries are sent through Pipeworx's third-party MCP gateway.

Mitigation: Use only non-confidential queries and avoid patient identifiers, proprietary research, and sensitive business data.

Risk: Clinical, safety, and regulatory outputs may be incomplete, outdated, or unsuitable as a sole decision source.

Mitigation: Verify medical and regulatory conclusions against official sources before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-pharma-analyst)
- [Publisher profile](https://clawhub.ai/user/brucegutman)
- [ClinicalTrials.gov](https://clinicaltrials.gov/)
- [openFDA](https://open.fda.gov/)
- [RxNav API](https://lhncbc.nlm.nih.gov/RxNav/APIs/)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or text responses with JSON MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on third-party gateway availability and the upstream public data sources queried.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
