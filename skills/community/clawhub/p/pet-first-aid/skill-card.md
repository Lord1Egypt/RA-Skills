## Description:

Emergency first aid and health assessment guidance for dogs and cats when a pet is injured, choking, may have eaten something toxic, is overheating, or the owner needs to decide whether to seek emergency veterinary care.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External pet owners use this skill to triage dog and cat emergencies, follow basic first-aid steps, and identify when to contact an emergency veterinarian or animal poison-control professional.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests filesystem access even though pet first-aid advice should not normally require local file access.

Mitigation: Review the permission request before installation and deny or remove filesystem access unless a deployment-specific need is documented.

Risk: The install command uses an unpinned npx ClawHub installer.

Mitigation: Install only from a trusted ClawHub release and prefer a pinned version or verified release artifact.

Risk: Pet first-aid guidance can be harmful if treated as a substitute for urgent veterinary care.

Mitigation: Use the skill as supplemental guidance and contact an emergency veterinarian or animal poison-control professional immediately in real emergencies.

## Reference(s):

- [American Veterinary Medical Association Emergency Care](https://www.avma.org/resources-tools/pet-owners/emergencycare)
- [ASPCA Animal Poison Control](https://www.aspca.org/pet-care/animal-poison-control)
- [PetMD Emergency Guides](https://www.petmd.com)
- [Merck Veterinary Manual](https://www.merckvetmanual.com)

## Skill Output:

**Output Type(s):** [guidance, text, markdown]

**Output Format:** [Markdown and plain-text emergency guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include step-by-step triage, first-aid checklists, and escalation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
