## Description: <br>
LedgerAI helps agents use the LedgerAI API for invoice processing, expense categorization, financial report generation, and receipt scanning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jbennett111](https://clawhub.ai/user/Jbennett111) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent users use LedgerAI to call a bookkeeping API for invoice parsing, expense categorization, report generation, and receipt OCR when handling financial documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial payloads and signup emails are sent to an external LedgerAI/Voss Consulting Group API. <br>
Mitigation: Use a dedicated API key, send only data approved for that provider, and review privacy and retention terms before processing confidential financial records. <br>
Risk: API keys and generated keys may be exposed through shared shell environments or stderr logs during auto-signup. <br>
Mitigation: Store keys in scoped environment variables or a secret manager, and avoid running auto-signup where stderr is broadly logged. <br>


## Reference(s): <br>
- [LedgerAI ClawHub release](https://clawhub.ai/Jbennett111/ledgerai) <br>
- [LedgerAI API key endpoint](https://anton.vosscg.com/v1/keys) <br>
- [LedgerAI invoice processing endpoint](https://anton.vosscg.com/v1/invoices/process) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LEDGERAI_API_KEY or LEDGERAI_EMAIL; API responses are returned by the LedgerAI service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
