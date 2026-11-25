## Description:

Turn a plain-language task description into a minimal prompt template — extracts {{variable}} placeholders, detects output format, assembles a ROLE/TASK/INPUT/CONSTRAINTS/OUTPUT scaffold. Use when the user asks to write or templatize a prompt for an LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nenadzivotic](https://clawhub.ai/user/nenadzivotic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and prompt authors use this skill to turn a plain-language task description into a reusable LLM prompt scaffold, then refine its placeholders, output shape, and constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation instructions use an unpinned `npx skills` package.

Mitigation: Review the package and use a pinned package version and immutable skill revision where available.

Risk: The security review is incomplete; only 2 of 4 components were fully inspected.

Mitigation: Review the full skill and its installation source before installing or using it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/nenadzivotic/skills/meta-prompt-architect-lite)
- [Publisher profile](https://clawhub.ai/user/nenadzivotic)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Prompt scaffold with ROLE, TASK, INPUT, CONSTRAINTS, and OUTPUT sections; CLI report in JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scaffold can contain candidate placeholders and warnings and needs task-specific refinement.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
