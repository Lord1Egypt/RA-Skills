## Description:

Pre Publish Security audits repositories before release to detect leaked credentials, dependency vulnerabilities, documentation placeholders, and release-blocking security issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solmas](https://clawhub.ai/user/solmas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to run quick, scheduled, or full security audits before pushes and releases, including secret, history, dependency, documentation, and license checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent Git hook installation can change future push behavior in a repository.

Mitigation: Review or modify the hook installer before use, preserve any existing hooks, and install it only on intended repositories.

Risk: The scanner can inspect user-level credential locations.

Mitigation: Remove or disable the ~/.git-credentials check and run audits with only the access needed for the target repository.

Risk: Unsafe handling around user-supplied paths can expose command or task handling issues.

Mitigation: Use trusted local repository paths only and avoid attacker-controlled path names.

Risk: Audit reports written under /tmp may contain sensitive findings.

Mitigation: Treat generated reports as sensitive, restrict access where possible, and delete them after review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/solmas/skills/pre-publish-security)
- [Artifact-declared project homepage](https://github.com/solmas/openclaw-pre-publish-security)
- [Artifact-declared contribution link](https://github.com/solmas/pre-publish-security)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, terminal output, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create markdown audit reports and install a Git pre-push hook when invoked.]

## Skill Version(s):

2.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
