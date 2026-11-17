## Description:

Mom.skill is a parenting co-pilot that tracks parent-reported feeding, sleep, crying, soothing, and milestone observations to help caregivers recall routines and generate care handoff summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realteamprinz](https://clawhub.ai/user/realteamprinz)

### License/Terms of Use:

MIT-0

## Use Case:

External caregivers use Mom.skill to log infant feeding, sleep, crying, soothing, and milestone observations, then ask for concise pattern-based reminders and care handoff summaries. The skill is a memory aid for parent-reported routines and is not medical advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive infant, allergy, sleep, location, and caregiver-routine details may be stored as local human-readable files.

Mitigation: Use the skill only on trusted devices and storage locations, restrict filesystem access, and delete the local baby profile folder when the records are no longer needed.

Risk: Multi-caregiver sharing boundaries are unclear.

Mitigation: Clarify which caregivers may access the profile before sharing it across people, devices, or synced folders.

Risk: Pattern-based responses may be mistaken for medical, diagnosis, or treatment advice.

Mitigation: Treat outputs as a memory aid only and escalate health concerns such as fever, persistent rash, poor intake, or urgent symptoms to a pediatrician or emergency care.

## Reference(s):

- [Soothing Techniques Reference](references/soothing-techniques.md)
- [Mom.skill ClawHub Listing](https://clawhub.ai/realteamprinz/skills/mom)
- [realteamprinz Publisher Profile](https://clawhub.ai/user/realteamprinz)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with local Markdown and JSONL record updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses parent-reported observations and persists baby profiles, daily logs, and soothing playbooks as local human-readable files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
