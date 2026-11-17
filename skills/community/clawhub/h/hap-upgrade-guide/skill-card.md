## Description:

Helps agents answer Mingdao HAP private deployment upgrade questions and generate executable standalone or cluster upgrade guides when the required deployment details are available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1447443432](https://clawhub.ai/user/1447443432)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to assess HAP private deployment upgrade paths, architecture support, required pre-upgrade and post-upgrade operations, and to generate Markdown and HTML upgrade runbooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated upgrade guidance can include high-impact administration commands for HAP services, Kubernetes, Docker, and databases.

Mitigation: Review generated commands against the official Mingdao documentation and run them only in a planned maintenance window with backups and a rollback plan.

Risk: Some generated examples execute remote scripts through curl-to-bash patterns without built-in integrity verification.

Mitigation: Download remote scripts first, verify them against trusted checksums or signatures when available, inspect the contents, and execute with least privilege.

Risk: MongoDB examples may place credentials in command lines or copied shell history.

Mitigation: Use secure credential handling, avoid embedding passwords directly in command lines, and restrict database credentials to the minimum required privilege.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1447443432/skills/hap-upgrade-guide)
- [HAP documentation site structure reference](references/site-structure.md)
- [HAP upgrade command library](references/command-library.md)
- [HAP upgrade merge rules](references/merge-rules.md)
- [Mingdao private deployment version history](https://docs-pd.mingdao.com/version)
- [Mingdao private deployment upgrade detail pages](https://docs-pd.mingdao.com/upgrade/{version}/)
- [MongoDB 3.4 to 4.4 upgrade reference](https://docs-pd.mingdao.com/deployment/docker-compose/standalone/upgrade/mongodb/3.4_4.4)
- [MongoDB index rebuild reference](https://docs-pd.mingdao.com/deployment/components/mongodb/reIndex)
- [Object storage preset file reference](https://docs-pd.mingdao.com/faq/oss)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and HTML documents with inline shell commands, configuration snippets, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated upgrade guide files named with the source version, target version, and deployment mode.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
