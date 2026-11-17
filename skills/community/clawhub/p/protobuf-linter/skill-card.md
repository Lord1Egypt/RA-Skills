## Description:

Lint Protocol Buffer (.proto) files for style, naming, structure, compatibility, and best-practice issues across proto2 and proto3.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and API engineers use this skill to run a local Python linter against .proto files or compare old and new schemas for breaking changes before publishing protobuf changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports a denial-of-service parser bug and says security or compatibility coverage may be overstated.

Mitigation: Review before installing, use only on trusted or reasonably sized protobuf files until reserved-range handling is fixed, and do not treat reported coverage as comprehensive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/protobuf-linter)

## Skill Output:

**Output Type(s):** [Shell commands, Text, JSON, Guidance]

**Output Format:** [Markdown guidance with command examples; linter output can be text, JSON, or summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns exit code 0 when no errors are found, 1 when errors are found, and 2 for invalid input.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
