## Description:

Identify OEM part numbers from PDF parts catalogs by matching vehicle scope, exploded positions, and parts-table entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextaltair](https://clawhub.ai/user/nextaltair)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to identify OEM vehicle part numbers from PDF parts catalogs, especially when a requested component may only be sold as part of an assembly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may download and process third-party PDF catalogs.

Mitigation: Use reputable catalog sources when possible and avoid untrusted PDFs.

Risk: Catalog snippets or extracted text can lead to incorrect part-number attribution when vehicle scope, diagram position, or table row context is incomplete.

Mitigation: Confirm the catalog header, subsystem title, diagram position, table position, side, quantity, and variant before reporting the part number.

Risk: A requested component may not be sold separately and could be listed only within a larger assembly.

Mitigation: Report the smallest catalog-listed assembly that contains the component, and state that no standalone row was found when supported by the catalog evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nextaltair/skills/oem-parts-catalog-identification)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown response with catalog URL and relevant PDF page citations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include concise PDF inspection steps and part-table evidence such as position, side, quantity, variant, and assembly relationship.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
