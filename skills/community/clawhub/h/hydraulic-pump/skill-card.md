## Description:

Guides users through generating hydraulic-pump CAD drawings by collecting design parameters, calling JixieTools calculation APIs, and creating a guest production sheet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liv09370](https://clawhub.ai/user/liv09370)

### License/Terms of Use:

MIT-0

## Use Case:

External users and engineering agents use this skill to collect hydraulic pump design inputs, review calculated parameters, and request CAD drawing generation through a third-party production workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hydraulic-pump design parameters are sent to jixietools.com and a guest-accessible production link is created.

Mitigation: Confirm user consent before submitting parameters, avoid sensitive data, and treat generated filenames and guest links as sensitive.

Risk: The skill includes shell command templates that could be unsafe if raw user input is inserted directly.

Mitigation: Use safe JSON serialization and shell-free HTTP calls where possible; otherwise validate and quote values before execution.

Risk: Generated production links depend on a third-party workflow with limited disclosure in the artifact.

Mitigation: Review the third-party service behavior and link-sharing expectations before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liv09370/skills/hydraulic-pump)
- [JixieTools API base](https://jixietools.com/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with parameter tables, status updates, links, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce third-party guest production links and CAD generation status summaries.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
