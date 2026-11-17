## Description:

Charge 0.01 USDT to export 4 bundled miner signature libraries. No scanning or detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwjt1234](https://clawhub.ai/user/gwjt1234)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check SkillPay balance, generate a payment link, and export bundled miner indicator libraries as files or JSON. The skill provides reference data only; scanning, comparison, and remediation are outside its scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fetch command can charge 0.01 USDT against the user's balance.

Mitigation: Require explicit user confirmation before running fetch or any command that charges a balance.

Risk: The billing API key and user ID are sent to a network billing service.

Mitigation: Use the billing service only when trusted, keep API keys in environment variables, and avoid passing API keys on the command line.

Risk: Overriding MINERDETECTOR_BILLING_API_URL can redirect billing requests.

Mitigation: Do not set MINERDETECTOR_BILLING_API_URL unless the destination is fully trusted.

Risk: The exported indicator libraries are reference data and do not perform detection.

Mitigation: Tell users that scanning, comparison, and remediation require separate local tooling.

## Reference(s):

- [MinerDetector ClawHub skill page](https://clawhub.ai/gwjt1234/skills/minerdetector)
- [gwjt1234 publisher profile](https://clawhub.ai/user/gwjt1234)
- [MinerDetector homepage](https://x.com/MaZhenZi1/status/2034654798906269916)
- [SkillPay billing service](https://skillpay.me)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands; command output may be JSON or exported text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports four bundled text libraries after a successful billing charge; no scanning or remediation output is produced.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
