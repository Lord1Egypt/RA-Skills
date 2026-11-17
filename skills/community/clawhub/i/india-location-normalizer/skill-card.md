## Description:

Normalize Indian real-estate location text into canonical city and locality fields for Mumbai and Pune leads, with confidence scores and unresolved flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vishalgojha](https://clawhub.ai/user/vishalgojha)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill after lead extraction to standardize Mumbai and Pune real-estate locality hints before scoring or storage. It returns canonical city, locality, micro-market, matched alias, confidence, resolution method, and unresolved status without writing data or triggering outbound actions.

### Deployment Geography for Use:

India

## Known Risks and Mitigations:

Risk: Ambiguous aliases can route a lead to the wrong locality when the same short form is used for multiple areas.

Mitigation: Use the skill's unresolved_flag behavior for equally matched or low-confidence aliases, and review or tune ambiguous aliases such as bare "thane" and "cbd" before relying on routing decisions.

Risk: The alias map is limited to Mumbai and Pune, so unsupported cities or unrecognized locality text may remain unresolved.

Mitigation: Preserve the original input in matched_alias for unresolved records and treat unresolved outputs as requiring downstream review or expanded reference data.

## Reference(s):

- [India location aliases v1](references/india-location-aliases-v1.json)
- [Location normalizer input schema](references/location-normalizer-input.schema.json)
- [Location normalizer output schema](references/location-normalizer-output.schema.json)
- [ClawHub skill page](https://clawhub.ai/vishalgojha/skills/india-location-normalizer)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON object containing normalized location records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only normalization output with confidence scores, resolution method, and unresolved flags.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
