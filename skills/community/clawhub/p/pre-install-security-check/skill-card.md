## Description:

Security Check helps agents assess GitHub repositories, npm packages, PyPI packages, and downloaded shell scripts before installation by checking metadata, vulnerability sources, and heuristic risk signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gawezepobi09-debug](https://clawhub.ai/user/gawezepobi09-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review external repositories, packages, and install scripts before an agent proceeds with commands such as git clone, pip install, npm install, or curl-piped shell execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence whether an agent installs packages, clones repositories, or executes downloaded scripts based on heuristic signals.

Mitigation: Require manual confirmation before any install, clone, or curl-piped script, and treat a Safe label as advisory rather than permission to execute.

Risk: Mutable versions, unknown maintainers, and commands that execute downloaded code can remain risky even when metadata looks favorable.

Mitigation: Pin versions where possible, review maintainers and source changes, and require explicit approval for mutable or unfamiliar sources.

Risk: External vulnerability and package metadata sources may be incomplete, stale, unavailable, or rate limited.

Mitigation: Use multiple vulnerability sources, cache with a short freshness window, and fall back to manual review when security data cannot be retrieved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gawezepobi09-debug/skills/pre-install-security-check)
- [Skantek Approach](references/skantek-approach.md)
- [Vulnerability Databases](references/vulnerability-databases.md)
- [Adyen Skantek](https://www.adyen.com/blog/skantek)
- [Snyk Vulnerability Database](https://security.snyk.io)
- [GitHub Advisory Database](https://github.com/advisories)
- [Safety DB](https://github.com/pyupio/safety-db)
- [OSV Documentation](https://osv.dev/docs/)
- [npm Audit](https://docs.npmjs.com/cli/audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style risk summaries with command examples, risk labels, recommendations, and confirmation prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may classify targets as safe, review, or dangerous based on heuristic package, repository, and vulnerability signals.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
