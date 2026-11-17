## Description:

Search npm packages, inspect metadata and versions, review download stats, and check security advisories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, package maintainers, and security reviewers use this skill to search npm packages, inspect package metadata and versions, review download activity, and check advisories through npm registry tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the user to install and allow a third-party ClawLink plugin that can use an npm account, including private package data.

Mitigation: Install only if ClawLink is trusted, review permissions in the ClawLink dashboard, and prefer a least-privilege npm account or token.

Risk: Write operations such as token deletion or scope changes can affect npm account state.

Mitigation: Preview and explicitly confirm write operations before execution, and reject actions that do not match the user's intent.

## Reference(s):

- [npm Documentation](https://docs.npmjs.com/)
- [npm Registry API](https://github.com/npm/registry)
- [npm Security Advisories](https://www.npmjs.com/advisories)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON parameter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include npm package metadata, download statistics, advisory checks, connection guidance, and confirmation steps for write operations.]

## Skill Version(s):

1.0.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
