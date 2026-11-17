## Description:

Sets up and manages a long-running agent harness for complex, multi-session coding projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kzac313](https://clawhub.ai/user/kzac313)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to structure substantial coding projects into repeatable agent sessions with progress tracking, verification checkpoints, and per-feature commits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can run a generated init.sh script and make broad repository commits.

Mitigation: Use the skill in a clean branch or disposable clone, review init.sh before running it, and inspect git status and staged diffs before accepting commits.

Risk: Repository-local secrets or private files could be included in broad commits.

Mitigation: Keep secrets outside the repository or protected by .gitignore before using the skill.

## Reference(s):

- [Jumpstart Skill README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/kzac313/skills/jumpstart)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown instructions with JSON file specifications and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project scaffolding guidance for init.sh, feature_list.json, progress.txt, checkpoints, and git commits.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
