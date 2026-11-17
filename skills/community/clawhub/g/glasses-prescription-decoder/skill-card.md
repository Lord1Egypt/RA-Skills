## Description:

Explains eyeglass prescription fields, compares old and new prescriptions, and helps check values entered for glasses orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT-0

## Use Case:

People who receive eyeglass prescriptions can use this skill to understand the listed powers, compare a new prescription with an older one, and review values before ordering glasses. It is not intended for contact lens fitting or medical eye concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parsing or notation edge cases can produce incorrect signs, axis values, or derived lens powers that affect an order.

Mitigation: Have an optician verify signs, axis, and derived powers before ordering; check Unicode minus signs and plus-cylinder axis 180 carefully.

Risk: Saving a PD record writes an unencrypted local file and overwrites any existing record.

Mitigation: Save only when needed, protect the local file, and keep a separate copy if the existing record must be retained.

## Reference(s):

- [Eyeglass Prescription Reference](artifact/references/rx-science.md)
- [ClawHub release](https://clawhub.ai/voronindenis5/skills/glasses-prescription-decoder)

## Skill Output:

**Output Type(s):** [Text, JSON file, Shell commands, Guidance]

**Output Format:** [Plain text analysis and instructions; optional JSON pupillary-distance record]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prescription fields and optional prior prescription, pupillary distance, or working distance]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
