## Description:

Creates and pushes a GitHub Actions workflow that builds OpenClash installer packages for a user's iStoreOS fork.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veelove](https://clawhub.ai/user/veelove)

### License/Terms of Use:

MIT-0

## Use Case:

Developers maintaining iStoreOS forks use this skill to add a GitHub Actions workflow that builds OpenClash .run installer artifacts and publishes them from their repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for GitHub credentials and enables write-capable workflow permissions.

Mitigation: Use a fine-grained, single-repository, short-lived token or make the repository changes manually; avoid enabling repository-wide write permissions or workflow pull request approvals.

Risk: The workflow can publish privileged router installer binaries built from downloaded remote content.

Mitigation: Inspect the workflow before running it, pin and verify downloaded binaries, and review generated installers before using them on a router.

## Reference(s):

- [Build OpenClash workflow](references/build-openclash.yml)
- [ClawHub skill page](https://clawhub.ai/veelove/skills/istore-build-openclash)
- [OpenClash releases API](https://api.github.com/repos/vernesong/OpenClash/releases)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash commands and YAML workflow content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GitHub repository URL and GitHub token from the user; the generated workflow creates .run installer artifacts.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
