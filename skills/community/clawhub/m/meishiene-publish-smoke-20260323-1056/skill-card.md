## Description:

Verify ClawHub login, dry-run sync state, one-off publish success, and cleanup for a local skill workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meishiene](https://clawhub.ai/user/meishiene)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to confirm that ClawHub authentication, dry-run inspection, temporary publishing, and cleanup work end to end for a local workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the current authenticated ClawHub account to publish a temporary skill.

Mitigation: Confirm the expected account with `clawhub whoami` before publishing and use a clearly temporary slug.

Risk: A smoke-test skill could remain visible or registered after verification.

Mitigation: Review the dry-run and publish output, then run `clawhub hide` or `clawhub delete` for the temporary slug after the test.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meishiene/skills/meishiene-publish-smoke-20260323-1056)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance expects the agent or user to review command output and clean up the temporary published skill when verification is complete.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
