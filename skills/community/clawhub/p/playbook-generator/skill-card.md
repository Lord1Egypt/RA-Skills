## Description:

Generate playbook YAML files for the intelligent outbound call platform through natural language guided conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[npufwb](https://clawhub.ai/user/npufwb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to turn outbound-call business scenarios into structured YAML playbooks for import, testing, and iteration in an intelligent call platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated YAML may contain invalid identifiers, unsafe values, or references that do not match the target platform schema.

Mitigation: Preview the parsed YAML before import, validate playbook_id and intent references, and run the included validation checklist.

Risk: Generated playbooks may affect regulated collection, credit, insurance, or telesales workflows.

Mitigation: Review scenario language, compliance rules, and forbidden words with the appropriate business or compliance owner before use.

Risk: Saving generated playbook files can overwrite existing local playbook definitions if paths or identifiers collide.

Mitigation: Check the target file path and playbook_id before saving or importing generated output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/npufwb/skills/playbook-generator)
- [Publisher Profile](https://clawhub.ai/user/npufwb)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [YAML playbook content with Markdown validation checklist and next-step guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or display a playbook YAML file and includes checks for required schema fields, unique intent identifiers, and valid global fragment references.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
