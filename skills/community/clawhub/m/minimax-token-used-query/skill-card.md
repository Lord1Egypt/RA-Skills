## Description:

Queries a MiniMax Coding Plan page through a local Chrome browser session and reports token usage, reset timing, and quota details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljzxzxl](https://clawhub.ai/user/ljzxzxl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and MiniMax Coding Plan users can use this skill to check current token usage, reset time, and remaining quota before continuing work that depends on MiniMax capacity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reuse a real Chrome browser profile and operate an authenticated MiniMax session.

Mitigation: Run it only in a trusted local environment and review browser automation actions before relying on the result.

Risk: The release evidence says the skill can store a MiniMax password in a plaintext OpenClaw memory file.

Mitigation: Prefer an existing browser session or an OS keychain-backed secret store, and avoid persisting account passwords in plaintext.

Risk: The skill may request login factors and leave an account screenshot in /tmp.

Mitigation: Provide login codes only when intentionally initiating a quota check, and remove temporary screenshots after use.

## Reference(s):

- [MiniMax Coding Plan management page](https://platform.minimaxi.com/user-center/payment/coding-plan)
- [ClawHub skill page](https://clawhub.ai/ljzxzxl/skills/minimax-token-used-query)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Console text with a JSON quota summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports used_percent, reset_minutes, quota window, prompt allowance, and timestamp when available.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
