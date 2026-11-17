## Description:

Uses the gitcode-api Python SDK for GitCode REST automation, including installation, sync and async clients, repository-scoped helpers, runtime resource introspection, and bundled CLI helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trenza1ore](https://clawhub.ai/user/trenza1ore)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to write, explain, debug, and validate Python automation against the GitCode REST API. It helps agents choose sync or async client patterns, configure repository context, inspect available SDK methods, and run environment or CLI checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides installation of an unpinned Python package.

Mitigation: Use a dedicated virtual environment, pin and verify the gitcode-api package version, and review the package before installation.

Risk: The skill can help perform broad authenticated GitCode operations, including destructive or sensitive repository, member, webhook, OAuth, key, merge, and file changes.

Mitigation: Use a least-privilege short-lived GitCode token from an environment variable or secret store, confirm the exact owner, repository, and intended action, and review sensitive operations before execution.

Risk: Passing access tokens through command-line arguments can expose credentials.

Mitigation: Prefer environment variables or a secret store over argv for GitCode tokens.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/trenza1ore/skills/gitcode-api)
- [GitCode API Reference](references/api-reference.md)
- [GitCode API Workflow Patterns](references/workflow-patterns.md)
- [Hosted SDK Quickstart](https://gitcode-api.readthedocs.io/en/latest/sdk/quickstart.html)
- [Client API Documentation](https://gitcode-api.readthedocs.io/en/latest/sdk/client_api.html)
- [Built-in CLI Documentation](https://gitcode-api.readthedocs.io/en/latest/sdk/cli.html)
- [PyPI Project](https://pypi.org/project/gitcode-api/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose authenticated GitCode API calls and local environment checks that require user review before execution.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
