## Description:

Update Mihomo site routing rules from natural-language requests, rebuild the published subscription, and verify the live output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grey0758](https://clawhub.ai/user/grey0758)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and authorized infrastructure operators use this skill to convert natural-language Mihomo routing requests into canonical route rule changes, worker publication, subscription sync, and live endpoint verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change live routing infrastructure and local Mihomo runtime state.

Mitigation: Use it only by authorized operators for the named repository, Cloudflare Worker, published subscription domain, and local runtime.

Risk: Deploy, sync, runtime configuration, restart, commit, or push actions could publish unintended routing changes.

Mitigation: Require human confirmation and review diffs before those actions are executed.

Risk: A completed repository edit may still leave clients on stale subscription content.

Mitigation: Verify the live published endpoint with cache busting before reporting completion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/grey0758/skills/mihomo-subscription-route-publisher)
- [Publisher profile](https://clawhub.ai/user/grey0758)
- [Published subscription domain](https://rules.xiannai.me)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown status summary with routing changes, command evidence, file changes, publish status, live verification, and next actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed Mihomo rule lines, edited configuration paths, validation commands, deployment commands, and live subscription verification results.]

## Skill Version(s):

1.0.0 (source: server release metadata and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
