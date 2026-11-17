## Description:

Moves an existing test suite to e2e one slice at a time while keeping both suites running until each port is proven.

This skill is ready for commercial/non-commercial use.

## Publisher:

[e2e](https://clawhub.ai/user/e2e)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to migrate existing browser and mobile test suites to e2e incrementally. It helps preserve coverage by keeping the source suite in place and recording migration progress until each port is proven.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions include unpinned package downloads, so the installed versions may change.

Mitigation: Review package sources and pin versions before running setup commands.

Risk: Screenshots or other observations from model-backed tests may contain sensitive information, and scan coverage is partial because referenced material is missing.

Mitigation: Review the referenced material before enabling model-backed tests and avoid sending sensitive observations to a model; use sanitized test data where possible.

## Reference(s):

- [e2e migration documentation](https://e2e.com/docs/migrate)
- [ClawHub skill page](https://clawhub.ai/e2e/skills/migrate-to-e2e)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions, Shell commands, Markdown]

**Output Format:** [Migration guidance, code and configuration changes, shell commands, and a MIGRATION.md progress file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Works through one test-suite slice at a time and may include an optional defect check.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
