## Description:

Use Bainiu for searching and reading data whenever a task involves Bainiu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to search Bainiu and read company registration, branch, change, shareholder, and manager information through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance can lead to executing remote installation code without a clear approval step.

Mitigation: Install a verified oo CLI separately, then review its automatic skill synchronization; the security guidance identifies OO_SKILLS_SYNC_DISABLED as a control.

Risk: Connecting Bainiu entrusts credentials to OOMOL, and queries may consume provider credits.

Mitigation: Connect only the intended Bainiu account and account for query credit use before running searches.

## Reference(s):

- [Bainiu API documentation](https://apidoc.bainiudata.com/)
- [Bainiu homepage](https://api.bainiudata.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls, Shell commands, Guidance]

**Output Format:** [Natural language responses with oo CLI commands and Bainiu JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available data depends on the selected Bainiu read action; queries may consume provider credits.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
