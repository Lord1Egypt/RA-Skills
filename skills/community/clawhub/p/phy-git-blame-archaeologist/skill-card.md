## Description:

Git history archaeology tool that helps developers explain why code exists by tracing blame, commit history, rename history, commit messages, linked references, and mystery blocks in a local git repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to investigate file, line, symbol, or directory history in a local git repository and produce a narrative explanation of why the code changed. It is useful for debugging, onboarding, maintenance, and documenting unexplained code decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to inspect local git history and nearby repository files while answering code-history questions.

Mitigation: Invoke it with an explicit file, line, symbol, commit, or directory so the investigation stays scoped to the intended repository area.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-git-blame-archaeologist)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown report with command snippets, timelines, findings, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally against a git repository and may inspect commit history plus nearby repository files when requested.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
