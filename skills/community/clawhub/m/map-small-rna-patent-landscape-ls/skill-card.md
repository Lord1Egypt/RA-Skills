## Description:

Build a company or portfolio-level patent landscape for small-RNA therapeutics from a supplied patent list or defined search scope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts and patent strategy teams use this skill to create traceable small-RNA patent landscapes from supplied patent identifiers or a reproducible discovery scope. It guides generation of patent evidence records, structured JSON/CSV analysis, XLSX workbooks, and self-contained HTML timelines for portfolio review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be used with confidential company, portfolio, or patent-analysis scope information.

Mitigation: Confirm confidentiality requirements and external-service permissions before retrieval or analysis, and use supplied authoritative records when live services are not approved.

Risk: Patent legal status, enforceability, term, FTO, infringement, validity, or patentability conclusions could be overstated if treated as legal advice.

Mitigation: Use the skill as a landscape and strategy workflow, verify material legal status in official registers, and route legal conclusions to qualified counsel.

Risk: Automated tagging or opportunity markers could imply unsupported portfolio gaps or strategy conclusions.

Mitigation: Require evidence locators, confidence, reviewer state, counterevidence, and explicit uncertainty for tags, strategy findings, and opportunity hypotheses.

Risk: Local scaffold creation writes project files and can affect an existing workspace.

Mitigation: Use a new empty project directory; the scaffold script refuses non-empty project directories and absolute project paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/map-small-rna-patent-landscape-ls)
- [Small-RNA Patent Tag Taxonomy](references/tag-taxonomy.md)
- [Small-RNA Patent Landscape Workbook Schema](references/workbook-schema.md)
- [Multidimensional Small-RNA Patent Timeline Specification](references/html-dashboard.md)
- [PatSnap patent search MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [PatSnap patent briefing MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured file specifications for Markdown evidence records, JSON/CSV analysis layers, XLSX workbooks, HTML reports, and project-scaffold configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates scoped local patent-landscape project files when the scaffold script is used; patent retrieval depends on authorized external services or supplied authoritative records.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
