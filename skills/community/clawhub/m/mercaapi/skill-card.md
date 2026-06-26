## Description: <br>
Helps agents use an unofficial Mercadona product API for product lookup, fuzzy search, category browsing, nutrition calculations, receipt scanning, and issue reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m0wer](https://clawhub.ai/user/m0wer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search Mercadona products, retrieve nutrition data, calculate portions, and match receipt items to product records for grocery or meal-planning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Receipt scanning can send uploaded receipt images, PDFs, or receipt URLs to mercaapi.sgn.space and an external AI service. <br>
Mitigation: Avoid submitting receipts with payment details or personal information unless that external processing is acceptable. <br>
Risk: Fuzzy product search can return unrelated products when match scores are low. <br>
Mitigation: Review the top matches and verify product names, categories, and nutrition fields before using them in calculations. <br>


## Reference(s): <br>
- [Mercadona Products API docs](https://mercaapi.sgn.space/api/docs) <br>
- [Mercadona Products API OpenAPI schema](https://mercaapi.sgn.space/openapi.json) <br>
- [ClawHub skill page](https://clawhub.ai/m0wer/mercaapi) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Code] <br>
**Output Format:** [Markdown with endpoint examples, JSON schemas, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No authentication required; receipt scanning can involve uploaded files or URLs sent to the external API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
