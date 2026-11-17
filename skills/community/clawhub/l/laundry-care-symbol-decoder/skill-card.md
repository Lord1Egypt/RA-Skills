## Description:

Decode clothing care symbols into a one-garment or batch care sheet with symbol meanings, actions, avoid notes, delicate-fabric warnings, and label-readability flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn clothing tag symbols or batch garment labels into a printable laundry care sheet with meanings, actions, avoid notes, and conservative warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases could activate the skill for general washing-instruction requests.

Mitigation: Review and narrow trigger phrases if accidental activation matters in the deployment environment.

Risk: Version metadata differs between server release and skill.json at 1.0.1 and SKILL.md or ACCEPTANCE.md at 1.0.0.

Mitigation: Reconcile artifact version fields before publisher cleanup or downstream release notes are finalized.

Risk: Garment care guidance can be wrong when labels are unreadable, missing, contradictory, or when fabric is delicate.

Mitigation: Keep label and fabric details authoritative, mark uncertain symbols as needing confirmation, prefer gentler care, and recommend professional cleaning for high-risk items.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/laundry-care-symbol-decoder)
- [Publisher Profile](https://clawhub.ai/user/harrylabsj)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown care sheet with tables and short action lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only output; no executable code, API calls, credentials, persistence, or network-dependent assets are evidenced.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill.json; SKILL.md and ACCEPTANCE.md list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
