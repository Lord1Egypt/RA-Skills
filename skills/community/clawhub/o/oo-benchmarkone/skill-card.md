## Description:

Operate BenchmarkONE to read, create, and update data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

BenchmarkONE account users can use the skill to search contacts, list account options, create contacts, and update contacts through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup recommends running remote CLI installer scripts that have not been verified.

Mitigation: Verify the CLI release source and inspect the installer before running it.

Risk: BenchmarkONE requests and data pass through OOMOL, while the live connector implementation remains unverified.

Mitigation: Review the setup and data handling before use, send only data needed for each action, and retain confirmation for contact changes.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [BenchmarkONE](https://www.benchmarkone.com/)
- [BenchmarkONE API documentation](https://help.benchmarkone.com/en/articles/2383067-api-documentation-for-advanced-users)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [JSON connector requests and responses with shell commands and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read account data or create and update contacts.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
