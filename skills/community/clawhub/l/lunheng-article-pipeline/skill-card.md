## Description:

A multi-agent workflow for researching, drafting, auditing, and reviewing academic papers, long-form articles, and industry analyses, with advisory publication-channel recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyunlai](https://clawhub.ai/user/zuoyunlai)

### License/Terms of Use:

MIT

## Use Case:

Writers, researchers, and analysts use this skill to develop sourced long-form work through coordinated research, drafting, critique, and peer-review stages. It produces publication-readiness assessments and advisory journal or channel matches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow creates many files and may spawn worker sessions.

Mitigation: Review the Phase 0 choices and project scope before allowing file creation or worker dispatch.

Risk: Optional research searches, academic metadata, Firecrawl, or operational telemetry may send queries or URLs to external services.

Mitigation: Review and explicitly choose the relevant Phase 0 consent options; avoid all-auto mode when individual approvals are needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zuoyunlai/skills/lunheng-article-pipeline)
- [Pipeline user guide](references/pipeline-readme.md)
- [Workflow overview](references/_shared/真源/pipeline-overview.md)
- [External services and consent](references/_shared/真源/external-services.md)
- [Deliverables](references/deliverables.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance, Files]

**Output Format:** [Markdown articles, research notes, audit and review reports, and publication recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates multiple project files; publication and journal matches are advisory.]

## Skill Version(s):

2.18.1 (source: ClawHub release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
