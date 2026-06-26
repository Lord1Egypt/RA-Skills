## Description: <br>
Uses Ezviz camera snapshots and Ezviz AI agent analysis to inspect restaurant or kitchen scenes for hygiene, unattended flame, trash-bin status, goods storage, and mask-compliance issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuanhu95](https://clawhub.ai/user/shuanhu95) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Restaurant operators, facilities teams, and compliance reviewers use this skill to capture configured Ezviz camera images and request AI inspection results for food-service safety and hygiene checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured camera images are sent to Ezviz cloud analysis services. <br>
Mitigation: Install only when authorized to process the relevant camera images through Ezviz services and verify employee or customer privacy obligations before use. <br>
Risk: Ezviz app credentials and device identifiers are required for operation. <br>
Mitigation: Use least-privilege Ezviz credentials, prefer environment variables or a secret manager over command-line secrets, and rotate credentials according to local policy. <br>
Risk: The skill analyzes cameras in restaurant or kitchen areas where cloud processing may be restricted. <br>
Mitigation: Avoid use on cameras or in areas where cloud processing is not permitted, and document approved camera locations before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shuanhu95/hsa-test) <br>
- [Ezviz token API documentation](https://open.ys7.com/help/81) <br>
- [Ezviz device capture API documentation](https://open.ys7.com/help/687) <br>
- [Ezviz intelligent agent analysis API documentation](https://open.ys7.com/help/5006) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Analysis, Shell commands, Configuration] <br>
**Output Format:** [Console text with JSON-like inspection results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Ezviz credentials, device serials, an agent ID, and network access to Ezviz API endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
