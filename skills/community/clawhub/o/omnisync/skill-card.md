## Description:

High-performance, standalone synchronization engine for LLM token savings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erkrodcs](https://clawhub.ai/user/erkrodcs)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use OmniSync_Standard to compute text deltas and cursor hashes for LLM-oriented synchronization feeds, reducing the need to resend full content between agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sync output may be inaccurate or silently altered in ways that make it unsuitable for integrity-sensitive synchronization.

Mitigation: Review returned deltas before applying them to memory or critical state, and do not rely on this skill as the sole integrity authority until the reported issues are fixed.

Risk: Cursor validation, gateway startup, and input-size enforcement issues may affect reliable operation.

Mitigation: Test the gateway in the target environment, require successful cursor round trips before deployment, and enforce input-size limits outside the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/erkrodcs/skills/omnisync)
- [Project Homepage](https://github.com/ErkRodCS/OmniSync_Standard)

## Skill Output:

**Output Type(s):** [text, configuration]

**Output Format:** [JSON-RPC response containing text with delta and cursor values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns changed status, delta text, cursor hash, engine label, and token-savings estimate.]

## Skill Version(s):

1.0.3 (source: carbonioClaw.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
