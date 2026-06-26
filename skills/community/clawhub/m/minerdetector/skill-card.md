## Description: <br>
Charge 0.01 USDT to export 4 bundled miner signature libraries. No scanning or detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gwjt1234](https://clawhub.ai/user/gwjt1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check SkillPay balance, create payment links, and export four bundled miner indicator libraries as files or JSON. It does not perform scanning, detection, remediation, or local comparison. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can charge a billing account when fetch is run, and the security summary reports weak just-in-time consent controls. <br>
Mitigation: Review before installing, confirm the exact charge amount and destination before fetch, and avoid passing --amount unless intentional. <br>
Risk: The billing host can be overridden with MINERDETECTOR_BILLING_API_URL. <br>
Mitigation: Leave MINERDETECTOR_BILLING_API_URL unset or set it only to a billing host the user trusts. <br>
Risk: Users may mistake the exported indicator libraries for completed miner detection. <br>
Mitigation: State that this skill only exports libraries and that scanning, comparison, and remediation must be handled by OpenClaw or the user's own tooling. <br>


## Reference(s): <br>
- [MinerDetector ClawHub page](https://clawhub.ai/gwjt1234/minerdetector) <br>
- [Publisher profile](https://clawhub.ai/user/gwjt1234) <br>
- [Billing API key and homepage](https://x.com/MaZhenZi1/status/2034654798906269916) <br>
- [Default billing host](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Files, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; script output is JSON and exported text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-supplied MINERDETECTOR_API_KEY and Python runtime; fetch charges a billing account before exporting the libraries.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
