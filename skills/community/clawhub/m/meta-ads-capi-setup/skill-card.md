## Description: <br>
A Meta Conversions API setup guide for configuring server-side event tracking to improve Meta Ads conversion measurement and reduce CPA discrepancies versus pixel-only tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elias-didoo](https://clawhub.ai/user/elias-didoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operations teams, developers, and external agencies use this skill to set up Meta Conversions API tracking, choose an integration method, configure conversion events, test deduplication, and handle customer identifiers responsibly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meta system-user tokens and pixel identifiers can be exposed if copied into code, logs, shared documents, or repositories. <br>
Mitigation: Store access tokens like passwords, use environment variables or a secrets manager, restrict token permissions to the minimum required scopes, and rotate tokens when access changes. <br>
Risk: Sending hashed identifiers, CRM status, or revenue events to Meta without appropriate consent or another lawful basis can create privacy and compliance risk. <br>
Mitigation: Confirm the lawful basis before sending data, minimize transmitted fields, honor opt-outs, and update privacy disclosures for server-side conversion tracking. <br>
Risk: Incorrect Pixel and CAPI event setup can duplicate, omit, or misattribute conversion events. <br>
Mitigation: Test events in Meta Events Manager, pass the same event_id for browser and server events, verify deduplication status, and monitor parameter completeness before relying on campaign metrics. <br>


## Reference(s): <br>
- [Meta Graph API CAPI events endpoint](https://graph.facebook.com/v21.0/{pixel_id}/events) <br>
- [ClawHub skill page](https://clawhub.ai/elias-didoo/meta-ads-capi-setup) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration] <br>
**Output Format:** [Markdown setup guide with credential tables, event checklists, and API endpoint guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Meta access token, pixel ID, Business Manager permissions, and privacy review before sending customer identifiers.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
