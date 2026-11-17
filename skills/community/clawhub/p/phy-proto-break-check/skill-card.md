## Description:

Protobuf/gRPC breaking change detector that compares .proto schema versions and reports critical, breaking, non-breaking, and note-level changes with migration guidance and a CI fail-gate command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and backend engineers use this skill before merging protobuf or gRPC schema changes to identify compatibility breaks across messages, fields, enums, services, and RPCs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker may read .proto files from selected directories or git refs and may run local git commands to inspect history.

Mitigation: Run it only against intended repositories and paths, and review command scope before using git-history based comparisons.

Risk: Detection accuracy is imperfect and findings may miss some protobuf compatibility issues.

Mitigation: Treat results as a compatibility aid, review findings manually, and combine with protobuf tooling such as buf lint or protoc validation when appropriate.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-proto-break-check)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style analysis with categorized findings, migration guidance, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CI fail-gate command suggestions for blocking critical or breaking protobuf changes.]

## Skill Version(s):

1.0.3 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
