## Description:

What tokens are whales dollar-cost averaging into? Jupiter DCA strategies by smart money and target token fundamentals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts and developers use this skill to review Solana Jupiter DCA activity attributed to smart money and investigate target tokens' fundamentals and flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research calls, including repeated calls in loops, may spend funds from the configured wallet when an eligible x402 payment challenge is accepted.

Mitigation: Review wallet authorization, payment policy, and spending limits before research; account for the possible cost of each call.

Risk: Retrying after an authentication failure through anonymous access could enter a separate paid workflow.

Mitigation: Stop on authentication or renewal failure, follow the CLI guidance, and use the documented account check when troubleshooting calls for it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/nansen-devops/skills/nansen-dca-tracker)
- [Nansen CLI browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and research findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research calls may incur usage charges; findings depend on available Nansen data and account entitlements.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
