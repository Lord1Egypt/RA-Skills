## Description:

A Chinese-language PRD writing helper that turns a core product requirement and North Star metric into a structured Markdown product requirements document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielniu](https://clawhub.ai/user/danielniu)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers and product teams use this skill to draft or improve PRDs from a short requirement, a North Star metric, and project context. For AI or algorithm projects, it adds sections for model capability, evaluation, prompt design, fallback behavior, and safety considerations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad PRD-related phrases.

Mitigation: Confirm the user wants a PRD draft and has provided or approved the North Star metric before generating the document.

Risk: Generated example PRDs may mention third-party integrations, data handling, or token-handling flows that have not been reviewed.

Mitigation: Review privacy, consent, credential handling, and integration requirements before implementing any generated PRD.

Risk: Generated requirements, metrics, timelines, and acceptance criteria may contain assumptions.

Mitigation: Have product, engineering, design, and QA reviewers validate the generated Markdown before using it as an implementation source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielniu/skills/prd-writter)
- [README.md](artifact/README.md)
- [Skill Manifest](artifact/manifest.md)
- [General PRD template](artifact/templates/prd-template.md)
- [AI project PRD template](artifact/templates/ai-prd-template.md)
- [Example PRD](artifact/examples/example-prd.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown PRD document with tables, checklists, and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output; general product and AI-project templates are selected according to the user's request.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
