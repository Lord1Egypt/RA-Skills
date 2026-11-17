## Description:

Creates and iterates enterprise software solution presentations as full-page PNG slides, with optional PPTX decks, outline materials, contact sheets, and too-large request handoff guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javastarboy](https://clawhub.ai/user/javastarboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, consultants, and enterprise presentation producers use this skill to plan, generate, review, repair, and package business solution decks built from full-page PNG slides. It is suited for customer-facing enterprise software solution narratives that need consistent title treatment, staged review, and optional PPTX assembly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may read shell profile configuration and send an API key to a configurable model endpoint.

Mitigation: Avoid automatically sourcing shell profiles; validate any custom OPENAI_BASE_URL, require HTTPS, and send API keys only to explicitly trusted providers.

Risk: The workflow can generate and modify many presentation assets under a workspace.

Mitigation: Keep outputs under the project workspace, stage generated files before approval, and review PNG/PPTX contents before replacing final deliverables.

Risk: Image model output may contain incorrect text, artifacts, or overbroad business claims.

Mitigation: Use the documented page-level quality checks, verify visible text and business boundaries, and require human review before customer-facing use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/javastarboy/skills/ppt-produce-bycodex)
- [PPT production guide](artifact/references/ppt-production-guide.md)
- [Enterprise Solution Title-Bar Template](artifact/references/titlebar-template.md)
- [Too-Large Handoff Template](artifact/references/too-large-handoff-template.md)
- [Author tutorial](https://www.yuque.com/lhyyh/ai/llm-wiki)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, generated PNG slide files, optional PPTX files, contact sheets, and supporting project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires workspace-scoped file staging and review before overwriting approved slide assets.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
