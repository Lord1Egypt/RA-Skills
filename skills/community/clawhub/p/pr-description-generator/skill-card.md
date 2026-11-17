## Description:

Auto-generates pull request descriptions from git diffs and commit history, with change categorization, impact analysis, reviewer hints, and markdown or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare PR bodies, summarize branch changes, and produce reviewer-ready descriptions from local git history and diffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects local git repositories and may summarize sensitive branch or working-tree changes.

Mitigation: Invoke it only for intended PR work, use narrow trusted --repo paths, and review generated text before sharing.

Risk: Optional --output and --copy modes can write generated PR text to disk or the clipboard.

Mitigation: Choose output paths deliberately and avoid clipboard use when working with sensitive repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/pr-description-generator)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown PR descriptions or JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports minimal, standard, and detailed templates, with optional file output or clipboard copy.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
