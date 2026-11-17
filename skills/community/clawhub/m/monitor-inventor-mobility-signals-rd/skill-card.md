## Description:

Monitors public patent records for inventor identity, organizational-association, and technical-adjacency signals that merit qualified review without inferring employment, resignation, misconduct, or legal risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Authorized IP, R&D, and legal-review teams use this skill to screen a company or named inventors over a defined period and prepare an evidence-backed public-patent briefing. The skill supports triage for qualified human review and must not be used for employee scoring, surveillance, or adverse employment action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Person-level monitoring may conflict with privacy, employment, works-council, access, retention, or jurisdiction requirements.

Mitigation: Use only for authorized IP, R&D, or legal review workflows after confirming purpose, jurisdictions, access controls, retention, and deletion requirements.

Risk: Patent records may be misread as proof of employment, resignation, misconduct, ownership, confidentiality breach, or legal risk.

Mitigation: Treat outputs as public-record triage only, preserve uncertainty and counterevidence, and route material decisions to qualified IP/legal and relevant HR or employment reviewers.

Risk: Identity matching, incomplete retrieval, and patent publication lag can produce false positives or false negatives.

Mitigation: Resolve identities using multiple evidence signals, document search coverage and cutoff limits, and use insufficient_evidence when identity or technical evidence cannot support review priority.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/yuanzhian-patsnap/skills/monitor-inventor-mobility-signals-rd)
- [Inventor mobility signal workflow](references/workflow.md)
- [Inventor mobility signal report schema](references/data_schema.json)
- [PatSnap patent search MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [PatSnap patent briefing MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown research protocol and validated HTML briefing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reviewed JSON is schema-checked, report content is escaped, and HTML output is not overwritten unless explicitly forced.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
