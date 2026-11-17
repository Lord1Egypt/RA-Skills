## Description:

Turns a plain-language task into a prompt scaffold with candidate input placeholders, a detected output format, and gaps for the user to resolve.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nenadzivotic](https://clawhub.ai/user/nenadzivotic)

### License/Terms of Use:

MIT-0

## Use Case:

Prompt writers and developers use this skill to turn a task description into a reusable LLM prompt template, then refine its placeholders, constraints, and output requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned installation may not reproduce the reviewed release.

Mitigation: Pin a reviewed release or commit when reproducible installs matter.

Risk: Short or underspecified tasks can produce generic or incomplete prompt scaffolds.

Mitigation: Resolve reported gaps with the user and review the template before using it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nenadzivotic/skills/meta-prompt-architect-lite)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown prompt scaffold with ROLE, TASK, INPUT, CONSTRAINTS, and OUTPUT sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Candidate input placeholders and warnings for missing details require user review.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
