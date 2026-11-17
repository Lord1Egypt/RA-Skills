## Description:

Manage Google Cloud Storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Google Cloud Storage tasks and automate storage-related cloud operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for a cloud storage credential and may expose STORAGE_API_KEY through shared shells, logs, or broad permissions.

Mitigation: Use a least-privilege credential limited to the intended storage actions, and avoid entering or logging the credential in shared environments.

Risk: The release evidence says the referenced implementation script is not included, so the operation scope is unclear.

Mitigation: Review the installed package contents and clarify the intended Google Cloud Storage actions before executing the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-gcp-storage-manager)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STORAGE_API_KEY for authenticated storage operations.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
