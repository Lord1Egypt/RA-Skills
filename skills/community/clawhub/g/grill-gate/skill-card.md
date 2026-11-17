## Description:

Runtime-level grill enforcement plugin. Blocks exec/spawn calls for research/development tasks unless a valid grill token exists. Ensures agents think before they act.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangsuann](https://clawhub.ai/user/tangsuann)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Grill Gate to require a design-review token before selected OpenClaw exec or sessions_spawn activity proceeds. It is intended as a workflow guard for research and development tasks that match configured trigger terms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The gatekeeper promise may be bypassed or forged if token issuance, token storage, one-time use, task binding, or bypass exemptions are weak.

Mitigation: Treat the skill as a lightweight workflow guard unless those controls are redesigned and reviewed for the installation.

Risk: The skill can block selected exec and sessions_spawn calls, which may interrupt normal agent workflows.

Mitigation: Install only where this blocking behavior is acceptable and configure triggers, exemptions, blocked commands, and token TTL for the intended workflow.

Risk: Dependency behavior can affect a security-sensitive installation.

Mitigation: Pin or audit dependencies before relying on the plugin in a sensitive environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tangsuann/skills/grill-gate)
- [Publisher profile](https://clawhub.ai/user/tangsuann)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [Plugin block or allow decisions with text guidance and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May block selected exec and sessions_spawn calls when no valid grill token is present.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
