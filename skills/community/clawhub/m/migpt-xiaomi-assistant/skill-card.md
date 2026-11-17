## Description:

Deploy MiGPT on a Xiaomi smart speaker to replace the built-in AI with a custom LLM-powered voice assistant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuituijcb](https://clawhub.ai/user/tuituijcb)

### License/Terms of Use:

MIT

## Use Case:

Developers and technically advanced users use this skill to deploy and troubleshoot a MiGPT-based custom voice assistant on Xiaomi or Redmi smart speakers, including device command configuration, login issues, latency tuning, and wake-word behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser cookies and reusable Xiaomi account tokens may be copied into scripts or plaintext local files.

Mitigation: Use the skill only on trusted, private systems; do not store Xiaomi cookies, passwords, passToken, ssecurity, or serviceToken values in shared, synced, or committed files.

Risk: The documented MIoT login workaround bypasses Xiaomi security verification and changes local authentication behavior.

Mitigation: Prefer supported Xiaomi login and device authorization flows or reviewed upstream fixes; apply bypass steps only when the account-security tradeoff is understood and accepted.

Risk: Debug or trace settings may expose environment variables, including API keys, in logs.

Mitigation: Keep debug and trace logging disabled in production and review logs before sharing or retaining them.

## Reference(s):

- [MiGPT Configuration Template](references/config-template.md)
- [MIoT Authentication Bypass via Browser Cookies](references/miot-auth-bypass.md)
- [Required Code Patches](references/patches.md)
- [End-to-End Latency Analysis](references/latency-analysis.md)
- [mi-gpt](https://github.com/idootop/mi-gpt)
- [mi-gpt issues](https://github.com/idootop/mi-gpt/issues)
- [MIoT Spec](https://home.miot-spec.com/)
- [mi-service-lite](https://www.npmjs.com/package/mi-service-lite)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with code blocks, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local package patch instructions and credential-handling guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
