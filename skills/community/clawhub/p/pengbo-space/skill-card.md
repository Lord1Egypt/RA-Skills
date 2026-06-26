## Description: <br>
Pengbo Space helps agents query Pengbo SMM services, select service IDs, place explicitly confirmed orders, check order status, request refills, and inspect account balance through pengbo.space/api/v1. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AmadoHallal](https://clawhub.ai/user/AmadoHallal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to configure a Pengbo Space API key, discover social media growth services, submit paid orders only after confirmation, and monitor order, refill, and balance state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid social-media growth orders can spend account balance or affect external social media targets. <br>
Mitigation: Review the service ID, target link, quantity, and expected cost before using add or refill, and require the documented --confirm flag for write actions. <br>
Risk: The Pengbo API key grants access to account operations. <br>
Mitigation: Store the key in PENGBO_API_KEY or pass it only at runtime, avoid sharing command transcripts containing secrets, and rotate the key if exposure is suspected. <br>
Risk: Local cache and audit logs can contain service, order, link, and activity details. <br>
Mitigation: Inspect retention needs and periodically clear local data files such as services caches and data/orders-log.jsonl when they are no longer needed. <br>
Risk: Maintenance scripts can install SBOM tooling or download signed update artifacts. <br>
Mitigation: Run release, SBOM, scan, and update helper scripts only as maintenance tasks, and apply updates only after signature verification succeeds. <br>


## Reference(s): <br>
- [Pengbo Space Skill Page](https://clawhub.ai/AmadoHallal/pengbo-space) <br>
- [Pengbo Space API Documentation](https://pengbo.space/user/api/docs) <br>
- [API Reference](references/api-reference.md) <br>
- [Security Release Checklist](references/security-release-checklist.md) <br>
- [Update Signing](references/update-signing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and structured JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports Chinese, English, Spanish, and mixed-language responses; write actions require explicit confirmation.] <br>

## Skill Version(s): <br>
1.1.1-beta.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
