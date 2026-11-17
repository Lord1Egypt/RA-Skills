## Description:

Automated API testing with Postman collections via Newman CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1999azzar](https://clawhub.ai/user/1999azzar)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to install Newman, run Postman collections from the command line, manage environments, generate reports, and integrate API regression or smoke tests into CI/CD pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled test runner command construction can execute injected shell input when called with untrusted arguments.

Mitigation: Review before installing, prefer a pinned release or verified package, and do not run scripts/run-tests.sh with untrusted arguments until the eval-based command construction is fixed.

Risk: Newman collections can target production or mutating APIs and may change external systems during test runs.

Mitigation: Confirm target APIs and environments before running tests, especially production or mutating collections.

Risk: Generated reports and webhook notifications may expose sensitive API details.

Mitigation: Restrict access to Newman reports and notification channels, redact sensitive values, and avoid publishing reports that contain secrets or private API data.

Risk: Installer and CI examples may fetch Newman packages without locked dependency versions.

Mitigation: Install Newman locally with locked dependencies or pin package versions in CI before using the skill in controlled environments.

## Reference(s):

- [Installation and Usage](artifact/INSTALLATION.md)
- [CI/CD Integration Examples](artifact/references/ci-cd-examples.md)
- [Advanced Newman Patterns](artifact/references/advanced-patterns.md)
- [Newman CLI Documentation](https://learning.postman.com/docs/running-collections/using-newman-cli/command-line-integration-with-newman/)
- [Newman Project](https://github.com/postmanlabs/newman)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline shell, JSON, YAML, Groovy, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Newman command lines, CI/CD snippets, report configuration, troubleshooting steps, and security-audit guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
