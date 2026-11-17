## Description:

Use this skill to read, create, and update Manatal recruitment records through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting teams and operators use the skill to retrieve candidates, jobs, organizations, and matches, and to create or update those records through a connected Manatal account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended CLI setup executes an unverified remote installer, and automatic skill synchronization may make broad, persistent changes.

Mitigation: Review and install the CLI separately, and explicitly control automatic skill synchronization before enabling the skill.

Risk: Manatal contains private recruitment records, and create or update actions change account data.

Mitigation: Connect the intended account and confirm the exact payload and effect before each write.

## Reference(s):

- [Manatal API documentation](https://developers.manatal.com/reference/getting-started)
- [Manatal](https://www.manatal.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON requests and structured Manatal responses, with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read records or create and update recruitment records.]

## Skill Version(s):

1.0.4 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
