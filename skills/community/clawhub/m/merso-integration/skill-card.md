## Description:

Integrate Merso PNPL (Play Now, Pay Later) payments into games or digital goods platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dreadterror](https://clawhub.ai/user/dreadterror)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Merso installment payments to games, apps, and digital goods platforms, including API authentication, purchase initiation, webhook handling, environment configuration, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook verification guidance can accept unsigned payment events, which may lead to incorrect granting or revoking of digital goods.

Mitigation: Before production use, require valid webhook signatures when available, reject missing or malformed signatures, use a dedicated webhook secret if Merso provides one, and verify payment state independently before changing entitlements.

## Reference(s):

- [Merso API Reference & Integration Guide](references/api.md)
- [Merso Commercial Context, Case Studies & Partner Info](references/commercial.md)
- [Merso Production API Base URL](https://api2.merso.io)
- [Merso Development API Base URL](https://api2.dev.merso.io)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with HTTP, JavaScript, SQL, environment-variable, and integration-checklist examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require MERSO_GAME_ID, MERSO_API_KEY, and MERSO_ENV for implementation guidance.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
