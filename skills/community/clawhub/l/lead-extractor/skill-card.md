## Description:

Extract structured real-estate lead records from parsed message objects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vishalgojha](https://clawhub.ai/user/vishalgojha)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to extract structured real-estate leads from parsed WhatsApp-style message data, including contact, budget, property, and listing-versus-requirement fields. It is intended to sit after message parsing and before India location normalization in a lead-processing workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may surface personal phone numbers and contact details from supplied chat data.

Mitigation: Install and use it only where extracting contact details from the supplied data is appropriate and authorized, and review outputs before using them elsewhere.

Risk: Extracted lead records may be incomplete or incorrectly classified.

Mitigation: Validate outputs against the bundled output schema and review field-level validation errors before downstream use.

## Reference(s):

- [Extraction Rules RE-India v1](references/extraction-rules-re-india-v1.md)
- [Parsed Message Input Schema](references/parsed-message-input.schema.json)
- [Output Leads Schema](references/output-leads.schema.json)
- [ClawHub Skill Page](https://clawhub.ai/vishalgojha/skills/lead-extractor)

## Skill Output:

**Output Type(s):** [JSON, guidance]

**Output Format:** [JSON array of validated lead objects or validation errors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lead records require lead_id, name, phone, and record_type; optional fields cover dataset mode, property details, budget, location hint, source, and timestamps.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
