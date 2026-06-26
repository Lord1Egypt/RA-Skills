## Description: <br>
Manage a Printful account through the Printful REST API using a private API token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sellers, ecommerce operators, and developers use this skill to inspect and manage Printful stores, synced products, manual/API-store products, orders, files, mockups, webhooks, shipping, tax, reports, and exports through authenticated API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authority over a live Printful account, including raw authenticated API requests. <br>
Mitigation: Install only when live account management is intended, use the least-privileged or store-scoped token available, and review raw requests before execution. <br>
Risk: Product deletion, order confirmation or cancellation, webhook changes, file uploads, and export paths can affect live business data or local files. <br>
Mitigation: Start with read-only commands, require manual review for sensitive mutations and export paths, and keep credentials in PRINTFUL_API_KEY rather than skill files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stanestane/printful-management) <br>
- [Printful API notes](references/printful-api-notes.md) <br>
- [Printful request examples](references/request-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration, markdown, code] <br>
**Output Format:** [Markdown guidance with shell commands, JSON request bodies, and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local markdown, CSV, or JSON exports when explicitly requested.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
