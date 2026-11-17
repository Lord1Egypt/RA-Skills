## Description:

Processes customs declaration documents by uploading invoices, packing lists, bills of lading, and related files to Leap, classifying document types, extracting structured declaration data, and generating a customs Excel result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axlemax](https://clawhub.ai/user/axlemax)

### License/Terms of Use:

Proprietary

## Use Case:

Trade operations users and customs-document agents use this skill to collect user-provided declaration documents, submit them to Leap for classification and extraction, review compliance guidance, and produce a standard customs Excel output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customs documents and generated declaration data may include sensitive commercial information and are sent to an external Leap service.

Mitigation: Install only when the user trusts DaoFei AI/Leap, confirm the exact files before upload, and restrict the agent runtime to the active task directory.

Risk: The LEAP_API_KEY credential authorizes access to the external service.

Mitigation: Configure the key through the platform's secure environment settings, avoid storing it in shell startup files, and rotate it if exposure is suspected.

Risk: List, cancel, and retry task controls may affect backend tasks beyond the immediate workflow if the service does not scope them to the current user.

Mitigation: Treat these task controls as privileged operations and use them only after confirming the target result_id and backend scoping behavior.

Risk: Excel modification in the final workflow depends on openpyxl, which may be installed dynamically.

Mitigation: Prefer a pinned or preinstalled openpyxl dependency before editing generated Excel files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/axlemax/skills/openclaw-skill-customs)
- [Leap service homepage](https://platform.daofeiai.com)
- [Leap Customs API Reference](artifact/references/API_REFERENCE.md)
- [File Types Reference](artifact/references/FILE_TYPES.md)
- [Compliance Rules](artifact/references/COMPLIANCE_RULES.md)
- [Field Guide](artifact/references/FIELD_GUIDE.md)
- [Industry Rules](artifact/references/INDUSTRY_RULES.md)
- [Interaction Guide](artifact/references/INTERACTION.md)
- [Modification Workflow](artifact/references/MODIFICATION.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell command blocks, JSON task responses, and generated Excel files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LEAP_API_KEY and network access to https://platform.daofeiai.com; Step 6 Excel edits may require openpyxl.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
