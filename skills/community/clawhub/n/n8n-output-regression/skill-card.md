## Description:

Run real n8n output regression tests with complete JSON fixtures and expected item counts, ordered IDs, fields or full JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blucca](https://clawhub.ai/user/blucca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow engineers use this skill to define expected outputs for n8n workflows and catch lost or changed items after edits or upgrades. It guides them through running the same regression case in the n8n editor or a network-isolated CLI/CI environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Docker image reference is not pinned to a tag or digest.

Mitigation: Review the runner image source and pin it to an approved immutable digest before running it.

Risk: Some local path references could not be resolved, so the security evidence is incomplete.

Mitigation: Review the skill and check unresolved local references before installation.

## Reference(s):

- [n8n-check project](https://github.com/blucca/n8n-check)
- [Complete invoice regression case](https://github.com/blucca/n8n-check/blob/main/examples/stop-after/case.json)
- [n8n editor test examples](https://github.com/blucca/n8n-check/tree/main/examples/editor-tests)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON configuration, Workflow test files]

**Output Format:** [Markdown instructions with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a reviewed regression case and an importable n8n editor test workflow or CLI/CI test artifacts.]

## Skill Version(s):

0.1.9 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
