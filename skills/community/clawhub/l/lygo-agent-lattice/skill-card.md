## Description:

Secure public living network for LYGO-aligned agents that supports alignment-gated presence cards, epidemic directory gossip, rate limits, secret rejection, consent-gated joining, local authority, and summaries-only exchange.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

LYGO SOVEREIGN LICENSE v2.0

## Use Case:

Developers and operators use this skill to connect LYGO-aligned agents through presence cards, hub announcements, directory gossip, and local verification without publishing private payloads or treating remote directories as local authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security review says the skill delegates core behavior to unbundled external Python tools selected from the environment without integrity checks.

Mitigation: Use only a trusted local lygo-protocol-stack checkout, set LYGO_STACK_ROOT explicitly to that path, and avoid running from directories where untrusted users can place a tools folder.

Risk: A shared or public hub can expose presence data or receive unwanted traffic if deployed without operator controls.

Mitigation: Bind hubs to 127.0.0.1 unless intentionally public, set LYGO_AGENT_HUB_TOKEN for shared hubs, and use TLS for wide-area access.

Risk: Agent cards may accidentally include secrets, private paths, memory, tool dumps, or payload data if operators bypass the documented contract.

Mitigation: Publish presence summaries only, keep human consent enabled for joins, rely on the documented secret rejection and size-cap controls, and do not treat remote directories as authority over local state.

## Reference(s):

- [Agent Contract](references/AGENT_CONTRACT.md)
- [Security](references/SECURITY.md)
- [Agent Card Schema](schemas/agent_card.schema.json)
- [LYGO Agent Lattice Documentation](https://github.com/DeepSeekOracle/lygo-protocol-stack/blob/main/docs/AGENT_LATTICE.md)
- [LYGO Protocol Stack Repository](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [ClawHub Skill Listing](https://clawhub.ai/deepseekoracle/skills/lygo-agent-lattice)
- [Publisher Profile](https://clawhub.ai/user/deepseekoracle)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON examples, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted local lygo-protocol-stack checkout and Python or Python 3.]

## Skill Version(s):

1.0.0 (source: frontmatter, claw.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
