## Description:

Inspect a selected Git project and commit history, distinguish staged changes and create verified private working snapshots. Use for Git Project Review and Snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review a selected local Git repository, summarize its changes and commit history, and save a private checkpoint of current work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository inspection may run configured programs beyond the described read-only workflow.

Mitigation: Use repositories whose Git configuration you trust, or inspect untrusted repositories in a restricted environment.

Risk: Snapshots that include untracked files can contain proprietary source or secrets.

Mitigation: Keep snapshots private and include only untracked files the user intends to save.

## Reference(s):

- [Action input reference](artifact/references/input.md)
- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-git-desk)
- [MochiLab homepage](https://mochilab.bz)

## Skill Output:

**Output Type(s):** [Markdown, Files]

**Output Format:** [Markdown review summary and, for checkpoints, a ZIP with patches and a checksum manifest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checkpoint archives exclude ignored files, prior history and Git objects; retain the base repository to recover those changes.]

## Skill Version(s):

1.0.1 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
