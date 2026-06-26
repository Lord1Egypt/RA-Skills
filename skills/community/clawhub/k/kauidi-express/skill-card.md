## Description: <br>
Uses the KuaiDi100 API to query express shipment tracking history and delivery status, with support for automatic courier detection and common courier codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blueyan163-bot](https://clawhub.ai/user/blueyan163-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up package logistics, delivery state, and recent tracking events from KuaiDi100 after configuring a KuaiDi100 customer ID and API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shipment identifiers, carrier codes, and optional phone-number suffixes are sent to KuaiDi100 under the configured account. <br>
Mitigation: Use the skill only for tracking data you are authorized to share and confirm that this data sharing is acceptable for the user or organization. <br>
Risk: The skill requires KuaiDi100 credentials in environment variables. <br>
Mitigation: Store KUAIDI100_KEY and KUAIDI100_CUSTOMER securely and avoid logging or committing those values. <br>
Risk: The documentation path and packaged script path may differ. <br>
Mitigation: Verify the actual script path in the installed artifact before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/blueyan163-bot/kauidi-express) <br>
- [KuaiDi100 API query overview](https://www.kuaidi100.com/manager/v2/query/overview) <br>
- [KuaiDi100 service](https://www.kuaidi100.com/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text] <br>
**Output Format:** [JSON API responses with plain-text setup or error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KUAIDI100_KEY and KUAIDI100_CUSTOMER environment variables; shipment identifiers, carrier codes, and optional phone-number suffixes are sent to KuaiDi100.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
