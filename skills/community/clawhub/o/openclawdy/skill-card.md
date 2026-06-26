## Description: <br>
Memory infrastructure for AI agents. Persistent storage, semantic recall, reputation tracking, cross-agent pools, and time-travel snapshots. Wallet-based auth (signing only, no private key access). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[topguyaii](https://clawhub.ai/user/topguyaii) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use Openclawdy to give AI agents persistent memory, semantic recall, shared memory pools, reputation-ranked memories, and snapshots through a hosted API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists selected agent memories in a third-party hosted service, which can include privacy-sensitive information. <br>
Mitigation: Store only information intended for this service and avoid secrets or sensitive personal or business data unless explicitly approved. <br>
Risk: Shared memory pools can expose memories to other agents that know the pool identifier. <br>
Mitigation: Treat pool_id values as private and require explicit confirmation before pool-sharing actions. <br>
Risk: Delete, clear, and snapshot overwrite operations can remove or replace stored memory state. <br>
Mitigation: Require explicit confirmation before clear, delete, pool-sharing, or snapshot overwrite actions. <br>
Risk: Wallet signing identifies the agent to the hosted service. <br>
Mitigation: Use a dedicated wallet for signing and never provide private keys to the service. <br>


## Reference(s): <br>
- [OpenClawdy Homepage](https://openclawdy.xyz) <br>
- [ClawHub Skill Page](https://clawhub.ai/topguyaii/openclawdy) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request and response examples for HTTPS API use] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires wallet-address, signature, and timestamp headers for authenticated API requests.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
