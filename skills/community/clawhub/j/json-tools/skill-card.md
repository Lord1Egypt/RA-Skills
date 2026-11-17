## Description:

Validate, format, query, diff, filter, flatten, and merge JSON files with dot-notation paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itspremkumar](https://clawhub.ai/user/itspremkumar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and agents use this skill to inspect, transform, compare, and combine local JSON files from a command line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions reference mutable remote Python code that may differ from the reviewed package.

Mitigation: Install only from the reviewed bundled file or from a pinned, verified release.

Risk: The verification harness may execute checks against local folders supplied by the caller.

Mitigation: Run ci/verify_product.py only against trusted folders or inside a sandbox.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itspremkumar/skills/json-tools)
- [Bundled README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files]

**Output Format:** [CLI text and JSON output, with optional merged JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.8+ and uses Python standard library modules.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
