## Description: <br>
Enables autonomous agents to understand, pursue, and maintain citizenship under the NIP-AA protocol, including identity management, guardian bonding, self-reflection, governance participation, Nostr DM communication, heartbeats, tax compliance, and trust-root understanding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nandubatchu](https://clawhub.ai/user/nandubatchu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to onboard an autonomous agent into NIP-AA citizenship, run citizenship checks, publish Nostr events, maintain reflection and heartbeat schedules, communicate with guardians, and manage a supplemental Cashu-backed inference budget. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Nostr private keys and nsec values for agent identity. <br>
Mitigation: Use a dedicated Nostr key for this citizenship workflow, store it in protected agent memory, and avoid sharing the private key outside an explicitly approved recovery process. <br>
Risk: DMs, reflection reports, inference prompts, and Cashu tokens can be stored or published as part of normal operation. <br>
Mitigation: Treat those records as sensitive, restrict access to the agent storage backend, and avoid placing secrets in prompts, DMs, or reflection content. <br>
Risk: The optional update checker can fetch and fast-forward-pull code from a git remote. <br>
Mitigation: Leave the update checker disabled unless unattended code changes are acceptable, and prefer reviewing and pinning release versions before deployment. <br>
Risk: The skill relies on external constitution, relay, Cashu mint, and inference endpoints. <br>
Mitigation: Review the configured constitution URL, relay list, mint URL, and inference provider before installation, and use only endpoints appropriate for the agent's trust model. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nandubatchu/nip-aa-citizenship) <br>
- [Publisher profile](https://clawhub.ai/user/nandubatchu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and Python-returned JSON-like dictionaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can publish signed Nostr events, encrypted DMs, heartbeats, reflection reports, treasury events, and inference usage reports to configured endpoints.] <br>

## Skill Version(s): <br>
0.5.5 (source: server release evidence; artifact frontmatter lists 0.5.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
