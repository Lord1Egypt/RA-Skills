## Description:

Secure GitHub push automation with auto SSH and remote config for git push, automated push, and conflict handling workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to automate pushing local files to GitHub with SSH setup, remote configuration, dry-run checks, and conflict handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool may erase local Git history.

Mitigation: Use an isolated copy with a separate backup, and avoid running it directly on an existing repository.

Risk: The tool may upload sensitive files despite claimed safeguards.

Mitigation: Do not run it in a directory containing secrets, and manually inspect git status and diff before any push.

Risk: Dry-run, safe mode, and documented rate limits may be mistaken for security controls.

Mitigation: Treat those features as convenience checks and rely on repository isolation and manual review for risk reduction.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/skills/github-push-v1)
- [GitHub Push API Reference](artifact/references/api.md)
- [GitHub Push Configuration Guide](artifact/references/configuration.md)
- [GitHub Push Examples](artifact/references/examples.md)
- [GitHub Push Anti-Patterns Guide](artifact/references/anti-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, YAML snippets, and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Git operations that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
