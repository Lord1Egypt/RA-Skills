## Description:

Create hard and symbolic links between files for file referencing, shortcuts, and directory organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to ask an agent for guidance or commands that create filesystem links for shared resources, shortcuts, and directory organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create local filesystem links, which may point into sensitive directories or replace expected paths if used carelessly.

Mitigation: Review target and link paths before use, avoid force replacement in sensitive directories, and execute only commands that match the intended path layout.

Risk: The documentation describes hard-link and force options, while the bundled script evidence only supports creating symbolic links.

Mitigation: Confirm the actual command or script behavior before relying on hard-link or force-replacement semantics.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, code]

**Output Format:** [Markdown with inline shell commands and file-linking guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local filesystem paths supplied by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
