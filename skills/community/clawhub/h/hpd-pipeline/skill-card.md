## Description:

HPD Pipeline guides an agent through a Planner, Designer, conditional Developer, and Tester workflow for approved HPD lab ideas, with Lobster-first orchestration and sequential fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omermesebuken1](https://clawhub.ai/user/omermesebuken1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and HPD lab operators use this skill to turn approved ideas into Turkish-first project briefs, BOMs, cost estimates, assembly plans, render prompts, optional software specifications, tester reports, artifact manifests, and completion summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated project plans, BOMs, cost estimates, render prompts, CAD concepts, code, or tester reports may be incomplete or inaccurate.

Mitigation: Review generated artifacts before use and rely on the skill's tester report and actual-vs-conceptual artifact checks before owner handoff.

Risk: The workflow may call image-generation tooling or a configured Gemini workflow when renders are requested.

Mitigation: Confirm tool configuration and review generated render outputs before treating them as deliverables.

## Reference(s):

- [HPD pipeline project contract](references/project-pipeline.md)
- [ClawHub skill page](https://clawhub.ai/omermesebuken1/skills/hpd-pipeline)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured sections and artifact paths when files are actually produced]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are Notion-first and primarily Turkish; render prompts may remain in English for image-generation tools.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
