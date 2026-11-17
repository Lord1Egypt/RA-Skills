## Description:

深度研究专业版 is an agent skill for enterprise research workflows covering team research, citation management, knowledge-base reuse, scheduled updates, AI-assisted analysis, and multi-format reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External teams, enterprise researchers, market analysts, academic groups, and consultants use this skill to organize deep research projects, manage citations, build reusable research knowledge bases, schedule recurring updates, and produce reports in Markdown, PDF, DOCX, or HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because the skill describes broad enterprise research behavior with generic triggers and under-scoped scheduled, REST API, and knowledge-base features.

Mitigation: Review the intended workflow before installation and require explicit approval before enabling scheduled jobs, API service mode, knowledge-base indexing, exports, or other broad automation.

Risk: The artifact describes command execution, package installation, API-key use, network research, and optional external service integrations.

Mitigation: Require approval for exec commands, pip installs, API-key access, and outbound data transfer; keep any REST API bound to localhost with access controls.

Risk: Research content, citations, knowledge-base exports, and generated reports may include sensitive or misleading material if sources or outputs are not reviewed.

Mitigation: Avoid sending sensitive research content unless intended, verify sources and generated conclusions, and review exported reports before distribution.

Risk: The artifact references scripts conceptually, but no implementation script was included.

Mitigation: Verify any script path, dependency, or generated command independently before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/in-depth-research-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, YAML configuration, and generated report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce structured status/result/error payloads and research outputs in Markdown, PDF, DOCX, HTML, BibTeX, or JSON depending on the selected workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
