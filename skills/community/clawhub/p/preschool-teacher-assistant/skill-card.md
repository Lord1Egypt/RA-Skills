## Description:

幼教百宝箱-AI幼师全流程助手 generates Chinese-language preschool lesson plans, observation records, family communication drafts, activity designs, teaching plans, classroom environment plans, teaching reflections, and children's stories, with optional interactive HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Preschool teachers and childcare staff use this skill to draft Chinese-language educational documents and classroom materials across common kindergarten workflows. It can operate from built-in templates or use an optional LLM provider when users provide an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Child-related classroom, student, or family information may be included in prompts or generated documents.

Mitigation: Prefer offline template mode for real student or family information, and remove names or identifying details before using LLM mode.

Risk: Optional LLM mode sends user-provided content to a configured external provider endpoint.

Mitigation: Use only trusted provider endpoints with provider-specific API keys, and review provider terms before sending sensitive content.

Risk: The skill writes standalone HTML reports that may contain user input or external model output.

Mitigation: Write reports to a dedicated output folder and treat generated HTML as untrusted when inputs came from users or an external model.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/preschool-teacher-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, HTML files, guidance]

**Output Format:** [Markdown, JSON, and standalone HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports offline template output and optional LLM-enhanced generation through user-supplied API settings.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill changelog, released 2026-06-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
