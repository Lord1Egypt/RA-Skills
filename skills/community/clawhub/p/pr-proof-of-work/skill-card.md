## Description:

TDD-driven E2E workflow with real Playwright browser screenshots as PR proof for issue-focused pull requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newtontech](https://clawhub.ai/user/newtontech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to turn one open issue into one pull request with test-first Playwright coverage, before/after screenshots, and a GitHub PR comment showing visual proof.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled screenshot publishing script can force-push to a GitHub remote.

Mitigation: Use only in trusted repositories, validate the selected remote and branch before running the script, and remove or constrain force-push behavior for shared repositories.

Risk: PR screenshot comments can expose sensitive UI state or local screenshot path details.

Mitigation: Review screenshots before publishing, avoid sensitive projects, use safe temporary files, and sanitize screenshot path names.

Risk: The workflow requires GitHub issue, PR, comment, commit, and push permissions.

Mitigation: Grant the agent only the repository permissions needed for the current PR and review generated commits and comments before merging.

## Reference(s):

- [Testing Patterns](references/testing-patterns.md)
- [PR-Proof-of-Work ClawHub Page](https://clawhub.ai/newtontech/skills/pr-proof-of-work)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local screenshot files and PR comment content when the bundled workflow is followed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
