## Description:

Use the oo CLI to read, create, update, and delete data in Dart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can inspect Dart task schemas and manage tasks through their connected account using oo CLI actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs internet-hosted installers whose contents and installed behavior are unverified.

Mitigation: Review and approve the CLI installation separately, including bundled skill changes, before allowing setup.

Risk: The OOMOL-connected account can be used to make changes or deletions in Dart.

Mitigation: Keep explicit approval controls for changes and deletions, and review the requested action before execution.

## Reference(s):

- [Dart](https://www.dartai.com)
- [Dart API documentation](https://app.dartai.com/api/v0/public/docs/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
