## Description:

Posts content to GitHub Gist and returns a shareable URL for rich context sharing between agents, operators, and humans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psiclawops](https://clawhub.ai/user/psiclawops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to publish reviewed markdown or text content to GitHub Gist and return a shareable URL for handoff or collaboration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may publish sensitive or internal content to a public GitHub Gist.

Mitigation: Review content before posting, prefer secret Gists for non-public material, and never include tokens, credentials, private logs, customer data, or internal context.

Risk: The GitHub token used for posting could be over-scoped or exposed.

Mitigation: Use a token with only the required gist scope, store it outside shared content, and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/psiclawops/skills/gist-post)
- [Project homepage](https://github.com/PsiClawOps/gist-share)
- [GitHub CLI](https://cli.github.com)
- [GitHub token settings](https://github.com/settings/tokens)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and a returned Gist URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GitHub CLI access and a GITHUB_TOKEN with gist scope.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
