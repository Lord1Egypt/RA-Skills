## Description: <br>
Omie ERP integration via API for managing clients, products, orders, invoices, financial accounts, stock, and webhook events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JAMESBOT-AGNT](https://clawhub.ai/user/JAMESBOT-AGNT) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and ERP operators use this skill to query Omie ERP clients, products, sales orders, invoices, financial accounts, and stock data, and to receive Omie webhook events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The webhook receiver can be exposed broadly and does not include built-in authentication. <br>
Mitigation: Run it only on trusted networks or behind authenticated ingress, restrict allowed sources, and avoid public exposure unless network controls are in place. <br>
Risk: Webhook handling logs full ERP event payloads, which may include sensitive business or personal data. <br>
Mitigation: Disable full payload logging, redact sensitive fields, and apply log retention and access controls before processing real ERP events. <br>
Risk: The skill uses Omie application credentials to access ERP data. <br>
Mitigation: Use least-privilege Omie app keys, store credentials in environment secrets, and rotate them if logs or runtime environments may have been exposed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Omie API credentials from OMIE_APP_KEY and OMIE_APP_SECRET environment variables.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
