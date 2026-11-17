## Description:

Searches local GitHub issue and pull request archives for related threads, duplicate clusters, sync freshness, and pull request status before live GitHub triage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclaw](https://clawhub.ai/user/openclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use Gitcrawl to inspect local OpenClaw GitHub issue and pull request archives, find related or duplicate threads, and verify live GitHub state before taking mutating triage actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Go install command uses @latest, so the installed gitcrawl version can change over time.

Mitigation: Pin or verify the exact gitcrawl module version before installation in controlled environments.

Risk: Cached issue and pull request archives can be stale or incomplete for decisions that mutate GitHub state.

Mitigation: Check archive freshness and verify the live GitHub issue or pull request state before labeling, closing, reopening, commenting, reviewing, or merging.

## Reference(s):

- [Gitcrawl homepage](https://github.com/openclaw/gitcrawl)
- [Gitcrawl ClawHub skill page](https://clawhub.ai/openclaw/skills/gitcrawl)
- [OpenClaw publisher profile](https://clawhub.ai/user/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gitcrawl CLI; live GitHub verification is expected before mutating actions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
