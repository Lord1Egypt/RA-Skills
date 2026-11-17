## Description:

PRD-Writer helps agents generate structured product requirements documents with guided requirement gathering, MoSCoW prioritization, Mermaid diagrams, and optional multi-perspective review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xx235300](https://clawhub.ai/user/xx235300)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, founders, and product teams use this skill to turn raw ideas, drafts, or requirement notes into structured PRDs with acceptance criteria, priorities, diagrams, and review sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML diagram attachments load Mermaid JavaScript from an unpinned third-party CDN and use permissive Mermaid rendering.

Mitigation: Review generated HTML before opening or sharing it, avoid using untrusted requirement text in diagram attachments, and prefer pinning or bundling Mermaid with integrity checks and stricter rendering settings before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xx235300/skills/prd-assistant)
- [Artifact README](artifact/README.md)
- [Chinese PRD template](artifact/PRD模板_中文.md)
- [English PRD template](artifact/PRD模板_英文.md)
- [Mermaid HTML template](artifact/HTML模板/mermaid_template.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [Markdown PRD content with Mermaid code blocks and optional HTML diagram attachment]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese, English, or bilingual output; selected mode controls document depth, diagrams, and review sections.]

## Skill Version(s):

3.0.0 (source: server release metadata and artifact templates)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
