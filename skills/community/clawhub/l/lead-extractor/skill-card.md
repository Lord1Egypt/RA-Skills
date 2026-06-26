## Description: <br>
Extract structured real-estate lead records from parsed message objects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vishalgojha](https://clawhub.ai/user/vishalgojha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users or agents use this skill to extract validated lead records from parsed WhatsApp real-estate messages, including contact details, budgets, listing or requirement type, deal type, location hints, and source text. <br>

### Deployment Geography for Use: <br>
India <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive real-estate lead data, including names, phone numbers, locations, budgets, and raw message text. <br>
Mitigation: Use it only with chat exports or parsed messages the user is authorized to process, and treat extracted output as sensitive. <br>
Risk: Extraction errors can misclassify listing and buyer requirement records or produce invalid lead fields. <br>
Mitigation: Validate inputs and outputs against the bundled schemas and review field-level validation errors before using the records downstream. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vishalgojha/lead-extractor) <br>
- [Extraction Rules RE-India v1](references/extraction-rules-re-india-v1.md) <br>
- [Parsed Message Input Schema](references/parsed-message-input.schema.json) <br>
- [Output Leads Schema](references/output-leads.schema.json) <br>
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text] <br>
**Output Format:** [JSON array of validated lead objects, or validation errors when records do not match the schema] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns only validated lead objects, uses strict input and output schemas, and avoids storage, summaries, outbound communication, or other side effects.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
