## Description:

Memory infrastructure for AI agents. Persistent storage, semantic recall, reputation tracking, cross-agent pools, and time-travel snapshots. Wallet-based auth (signing only, no private key access).

This skill is ready for commercial/non-commercial use.

## Publisher:

[topguyaii](https://clawhub.ai/user/topguyaii)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use Openclawdy to give agents persistent memory, semantic recall, shared memory pools, reputation tracking, and memory snapshots through a hosted external service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hosted service retains agent memory and may store sensitive facts, preferences, decisions, or context until explicitly deleted.

Mitigation: Avoid storing secrets or credentials, treat stored memories as sensitive, and use export or deletion endpoints when retention is no longer appropriate.

Risk: Shared memory pools can expose information to other agents that know or receive a pool ID.

Mitigation: Review what agents can write to shared pools and treat pool IDs as sensitive access material.

Risk: Vault clear and snapshot overwrite operations can remove or replace memory state.

Mitigation: Use destructive memory operations carefully and prefer read-only snapshot restore when inspecting historical memory state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/topguyaii/skills/openclawdy)
- [Openclawdy homepage](https://openclawdy.xyz)
- [Openclawdy API](https://openclawdy.xyz/api)
- [Openclawdy hosted skill definition](https://openclawdy.xyz/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with JSON API request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for using a hosted external memory service; API requests and responses use JSON.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
