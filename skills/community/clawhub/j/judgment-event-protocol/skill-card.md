## Description:

Verify JEP Core 0.7 signed event records and guide local creation or independent implementation testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[schchit](https://clawhub.ai/user/schchit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to verify JEP records, create signed records locally, and check implementation interoperability against conformance guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unverified package or running examples in an existing environment could expose local resources.

Mitigation: Verify the pinned package source and run examples in a fresh environment.

Risk: A valid signature alone does not establish truth, identity, or authorization for a real record.

Mitigation: Specify the actor, statement, and trust/profile rules before creating records; protect signing keys and apply acceptance checks before acting.

## Reference(s):

- [JEP Core homepage](https://github.com/hjs-spec/jep-core)
- [Local creation and independent verification example](https://github.com/hjs-spec/jep-agent-sdk#local-create--export--independent-verification)
- [BYOI conformance guidance](https://github.com/hjs-spec/jep-core/blob/main/docs/BYOI-CONFORMANCE.md)
- [Specification source map](https://github.com/hjs-spec/jep-core/blob/main/docs/SPECIFICATION-SOURCES.md)
- [ClawHub skill release](https://clawhub.ai/schchit/skills/judgment-event-protocol)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown with shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verification and conformance guidance; no bundled executable code.]

## Skill Version(s):

1.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
