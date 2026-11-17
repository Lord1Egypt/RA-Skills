## Description:

OpenClaw Team Builder helps agents manage OpenClaw teams by adding agents, deploying templates, checking health, fixing configuration, viewing org trees, rolling back changes, and suggesting team setups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eggyrooch-blip](https://clawhub.ai/user/eggyrooch-blip)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to inspect and update multi-agent team structure, role templates, channel bindings, health checks, rollback state, and goal-based team recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe credential handling and a confirmed local code-injection risk are reported by the security evidence.

Mitigation: Review commands before execution, avoid sharing real bot tokens or Feishu secrets in chat or shell history, test with throwaway credentials, and rotate any credentials already exposed.

Risk: Mutating commands can change persistent OpenClaw agent configuration, channel bindings, and trust relationships.

Mitigation: Use --yes, --fix, --rollback, and channel binding commands only after reviewing the planned change and checking the resulting team status.

Risk: Production OpenClaw setups may be impacted by automatic fixes, gateway restarts, or rollback operations.

Mitigation: Review the skill before production installation, run changes during a controlled window, and keep backups available before applying administrative operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eggyrooch-blip/skills/openclaw-team-builder)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw installation documentation](https://docs.openclaw.ai/install)
- [OpenClaw multi-agent documentation](https://docs.openclaw.ai/concepts/multi-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, json]

**Output Format:** [Markdown guidance with inline bash commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw 2026.3.0 or newer, python3, and macOS or Linux.]

## Skill Version(s):

3.6.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
