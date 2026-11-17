## Description:

Generates product-audience-content alignment tables for content e-commerce teams, translating product facts into consumer-facing language, shootable visuals, validation status, and competitor-reference notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[handsomeng](https://clawhub.ai/user/handsomeng)

### License/Terms of Use:

MIT-0

## Use Case:

External content e-commerce operators, product marketing managers, and content leads use this skill to align what a product is, who it is for, why the buyer acts, how to express selling points, and how competitor pain points should be handled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may keep local state or brand archives on disk, including a first-run marker and ljh-档案 files in the current directory.

Mitigation: Review expected file writes before installing, run in a workspace where local persistence is acceptable, and decline archive creation when persistent brand records are not desired.

Risk: The skill displays external WeChat community contact information during first use.

Mitigation: Review onboarding text before deployment and remove or replace external-contact promotion if it is not appropriate for the target environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/handsomeng/skills/ljh-duiqi)
- [ClawHub publisher profile](https://clawhub.ai/user/handsomeng)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Files]

**Output Format:** [Markdown alignment table with structured sections and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local onboarding and brand archive files when the user permits or the environment allows it.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact frontmatter lists 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
