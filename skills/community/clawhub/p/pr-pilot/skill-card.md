## Description:

Submit professional-quality pull requests and manage them through the full review lifecycle until merge or closure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sliverp](https://clawhub.ai/user/sliverp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create structured pull requests, monitor CI, respond to reviews, iterate on code, and track multiple open PRs across repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides repository mutation actions such as git pushes, PR creation, review comments, and PR tracking.

Mitigation: Review generated commands before execution and run them only in the intended repository, branch, and PR context.

Risk: The security guidance flags unsafe GitHub token handling patterns.

Mitigation: Authenticate GitHub CLI with gh auth login or a secure secret manager; avoid pasting tokens into chat or running literal export GH_TOKEN=<token> commands.

Risk: The security guidance flags a fixed /tmp/pr_body.md path for PR body files.

Mitigation: Use a secure temporary file or add a cleanup step when creating PR body files.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/sliverp/skills/pr-pilot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured PR templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PR URLs, CI status summaries, review responses, iteration steps, and updates to pr-tracker.md.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
