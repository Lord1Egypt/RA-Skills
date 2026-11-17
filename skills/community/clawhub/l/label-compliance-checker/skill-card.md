## Description:

Helps review medical-device label and instructions-for-use elements against a checklist based on Chinese labeling rules, producing decision-support results for human verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Medical-device labeling and quality teams use this skill to identify potentially missing label or instructions-for-use elements under Chinese medical-device labeling rules before human regulatory review. The bundled checker takes yes/no element inputs rather than analyzing full label text.

### Deployment Geography for Use:

Global (checks are framed around Chinese medical-device labeling rules)

## Known Risks and Mitigations:

Risk: The skill requests shell, file-write, and web-fetch access beyond what its label checklist clearly requires.

Mitigation: Restrict execution to the bundled checker and local label inputs; require explicit approval before fetching rules or writing files.

Risk: A checklist result could be mistaken for a regulatory determination, despite limited checks and unverified clause references.

Mitigation: Have a qualified reviewer verify conclusions against current official rules and the complete product documentation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/label-compliance-checker)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [JSON from the bundled command-line checker; human-readable decision support when used by an agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes missing-element flags and warnings; not a compliance certification or legal advice.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; source files list older versions)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
