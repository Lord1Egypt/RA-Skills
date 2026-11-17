## Description:

This skill captures images from Ezviz restaurant cameras and sends them to an Ezviz AI agent to inspect hygiene, unattended open flames, trash-bin status, goods storage, and mask compliance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuanhu95](https://clawhub.ai/user/shuanhu95)

### License/Terms of Use:

MIT-0

## Use Case:

Restaurant operators, kitchen safety teams, and chain managers use this skill to run AI-assisted inspections of kitchens, dining areas, canteens, and multi-location restaurant environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill captures and analyzes live camera imagery that may include employees, customers, or sensitive operational details.

Mitigation: Install only where camera capture and image analysis are authorized, and confirm privacy and legal requirements before use.

Risk: Ezviz app credentials, device serials, access tokens, and agent identifiers are sensitive and may be exposed through command-line history or verbose logs.

Mitigation: Prefer environment variables or a secret manager, avoid command-line secrets, rotate any secret previously exposed in shell history, and remove or gate debug logging before production use.

Risk: The skill depends on unpinned Python package installation and sends required inspection data to Ezviz services.

Mitigation: Pin dependencies for deployment review and confirm the organization accepts data transfer to the documented Ezviz endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shuanhu95/skills/hsa-test)
- [Ezviz token API documentation](https://open.ys7.com/help/81)
- [Ezviz device capture API documentation](https://open.ys7.com/help/687)
- [Ezviz intelligent agent analysis API documentation](https://open.ys7.com/help/5006)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Console text with JSON inspection results and Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Ezviz credentials, device serial numbers, an agent ID, the requests Python package, and network access to Ezviz endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
