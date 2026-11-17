## Description:

Build evidence-graded compound-target-disease network-pharmacology hypotheses for natural products, herbal medicines, formulae, and small molecules using live SciMiner tools plus public life-science evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sciminer](https://clawhub.ai/user/sciminer)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and life-science analysts use this skill to assemble evidence-graded compound, target, disease, pathway, and safety hypotheses for natural products, formulae, and small molecules. It guides SciMiner-backed analysis, evidence tables, interactive network reports, and reproducible handoffs without treating predicted or computational links as validated mechanisms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated network_report.html is active web content and has a browser-script injection risk from report input data.

Mitigation: Render reports only from trusted or reviewed node and edge tables, patch or harden the renderer before untrusted use, and avoid hosting generated reports on shared origins.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sciminer/skills/network-pharmacology)
- [SciMiner tool API index](https://sciminer.tech/tool_api_files/)
- [Evidence model](references/evidence-model.md)
- [SciMiner routing](references/sciminer-tool-routing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown narrative plus CSV, JSON, and HTML report artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCIMINER_API_KEY; every completed analysis must produce network_report.html.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
