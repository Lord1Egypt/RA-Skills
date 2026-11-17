## Description:

A local contract bus that connects cad-file-reader with quantity takeoff skills so they can reuse one drawing contract instead of parsing the same drawing again.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

MIT

## Use Case:

For developers and engineering teams, the bus shares a cad-file-reader contract and project state with connected quantity takeoff skills, so they can reuse one drawing's results across the workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports persistent host configuration changes and file deployment.

Mitigation: Inspect installer targets and configuration edits, run --dry-run, and test in a disposable Codex profile before applying.

Risk: The security review reports a missing advertised contract and a contract integrity weakness.

Mitigation: Confirm the required cad-contract/v1 files are present and validate the schema, provenance, and hashes; reject incomplete contracts for formal quantity workflows.

Risk: Security coverage is incomplete: 52 of 53 components were scanned, with one file partially inspected.

Mitigation: Review the incompletely inspected material before deployment and keep the release isolated until that review is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lisong2003-lgtm/skills/lis-skill-bus)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Local JSON project state and contract data, with shell commands and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bus connects and validates contract data; it does not parse drawings or calculate quantities.]

## Skill Version(s):

0.1.12 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
