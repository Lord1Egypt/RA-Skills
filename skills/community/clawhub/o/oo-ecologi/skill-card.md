## Description:

Use the Ecologi service to read environmental impact totals and purchase carbon avoidance, carbon removal, habitat restoration, and tree planting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users with a connected Ecologi account can check impact totals and make approved purchases of carbon avoidance, carbon removal, habitat restoration, or tree planting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback CLI setup runs a remote installer whose contents were unavailable for inspection.

Mitigation: Review the CLI installation separately and use a verified release.

Risk: Startup skill synchronization may make broader changes to agent skills.

Mitigation: Decide whether synchronization is needed; set OO_SKILLS_SYNC_DISABLED=1 to disable it.

Risk: Ecologi purchase actions spend funds and change account state.

Mitigation: Get approval for each purchase's exact amount and effect before execution.

## Reference(s):

- [Ecologi](https://ecologi.com)
- [Ecologi API documentation](https://docs.ecologi.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill listing](https://clawhub.ai/oomol/skills/oo-ecologi)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured action results with concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return impact totals; purchase actions require approval of the exact amount and effect.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
