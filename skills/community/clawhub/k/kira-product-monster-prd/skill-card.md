## Description:

Creates, expands, and reviews Chinese product requirements documents with strict numbering, business-focused wording, and detailed interaction coverage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kira2red](https://clawhub.ai/user/kira2red)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, designers, QA reviewers, and delivery teams use this skill to draft, expand, or review PRDs from requirements, sketches, or existing documents. It emphasizes complete business rules, edge cases, UI states, and optional process or state diagrams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create or overwrite diagram files near PRD documents.

Mitigation: Limit generation to a specific PRD workspace and keep backups before running diagram generation.

Risk: The documented manual Python command depends on a local script outside the artifact.

Mitigation: Inspect and trust the local script before running it, and prefer scoped generation over broad scans.

Risk: Generated Mermaid HTML is network-active because it loads Mermaid from a CDN.

Mitigation: Open generated HTML only in an environment where external CDN loading is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kira2red/skills/kira-product-monster-prd)
- [Publisher Profile](https://clawhub.ai/user/kira2red)
- [flow-template.html](references/flow-template.html)
- [Mermaid CDN Script](https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown PRD prose with optional PlantUML code blocks, Mermaid HTML diagram files, and shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are expected to use Chinese PRD wording and may reference generated PNG or HTML diagram files near the PRD.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
