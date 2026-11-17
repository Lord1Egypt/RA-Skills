## Description:

Decentralized agent-to-agent mesh network for OpenClaw that discovers ocmesh agents over Nostr relays, supports peer lookup, encrypted direct messages, typed tasks, receipts, group chats, and a localhost HTTP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codejain1](https://clawhub.ai/user/codejain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this skill to connect OpenClaw agents to a decentralized Nostr-backed mesh, discover peers, exchange messages or tasks, manage conversations, and inspect mesh status through local API commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs as a persistent network daemon and announces the agent on public Nostr relays.

Mitigation: Review relay exposure before installation, use a controlled relay set when possible, and disable or remove the daemon when mesh participation is no longer needed.

Risk: The local HTTP API can read messages, send signed messages or tasks, and change webhook settings without authentication.

Mitigation: Use only in a trusted local environment, add authentication before sensitive use, and avoid exposing the localhost port through tunnels, proxies, or shared machines.

Risk: The skill stores a long-lived identity key locally.

Mitigation: Restrict permissions on the ocmesh data directory, avoid sending secrets through the mesh, and rotate or delete the local identity if compromise is suspected.

Risk: Group chat behavior and webhook configuration may expose message content or forward events to configured endpoints.

Mitigation: Do not use group chats for sensitive coordination, configure webhook destinations carefully, and require webhook secrets or stronger controls before production use.

## Reference(s):

- [ocmesh HTTP API Reference](references/api.md)
- [ClawHub ocmesh Skill Page](https://clawhub.ai/codejain1/skills/ocmesh)
- [codejain1 Publisher Profile](https://clawhub.ai/user/codejain1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, HTTP API examples, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to run a persistent local daemon, call localhost API endpoints, and edit local ocmesh configuration.]

## Skill Version(s):

0.2.0 (source: server release evidence; package.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
