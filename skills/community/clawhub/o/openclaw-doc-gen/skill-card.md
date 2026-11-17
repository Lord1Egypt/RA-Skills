## Description:

Generates basic Python API documentation, updates README table-of-contents/API references, prints a simple Mermaid architecture diagram, and checks for missing documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use this skill to generate Markdown API documentation from Python source, update README navigation/API links, and check for missing documentation before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill overstates some documentation capabilities and may not fully implement every advertised feature.

Mitigation: Expect basic Python API documentation, README table-of-contents/API link updates, simple diagram output, and missing-documentation checks unless additional features are implemented.

Risk: Repository-writing workflows can modify README or documentation files.

Mitigation: Run on a test branch or clean diff, constrain source and output paths, and review generated changes before committing.

Risk: The included CI workflow example may not be safe to copy directly into a production repository.

Mitigation: Adapt CI steps to local review, permissions, and branch-protection requirements before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/michealxie001/skills/openclaw-doc-gen)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown documentation, shell command examples, and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated API documentation or README updates to user-specified repository paths; diagram and sync checks are basic.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
