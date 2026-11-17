## Description:

Search and read Granola meetings, notes, folders, and transcripts through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People who use Granola can find meetings, notes, folders, summaries, and transcripts through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A read-only request can trigger installation of an unverified CLI without a separate approval step.

Mitigation: Review and explicitly approve CLI setup before allowing installation; use a reviewed fixed release and consider disabling automatic skill synchronization.

Risk: Using the connected account gives OOMOL access to Granola meeting content.

Mitigation: Connect only the intended Granola account and consider what meeting content that account makes accessible.

## Reference(s):

- [Granola API documentation](https://docs.granola.ai/introduction)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Granola](https://www.granola.ai)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Structured Granola records returned as JSON, with readable text summaries or transcripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available data depends on the connected Granola account, plan, and action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
