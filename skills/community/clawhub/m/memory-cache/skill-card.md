## Description: <br>
High-performance temporary storage system using Redis for namespaced keys (mema:*), TTL management, session context caching, API-result caching, and data sharing between sub-agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1999AZZAR](https://clawhub.ai/user/1999AZZAR) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to store and retrieve temporary Redis-backed state, cache API results, and share data between sub-agents using the mema namespace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Redis configuration can expose cached data or retain it longer than intended. <br>
Mitigation: Configure Redis authentication, limit network exposure, use appropriate key prefixes, and apply TTLs for temporary context and cache entries. <br>
Risk: Unpinned dependency ranges may install unreviewed package versions. <br>
Mitigation: Use a reviewed lockfile or pinned dependency range before deployment. <br>


## Reference(s): <br>
- [Redis Key Naming Standards](references/key-standards.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/1999AZZAR/memory-cache) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and Redis key naming guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include Redis command results, JSON-formatted values when requested, and key-management guidance.] <br>

## Skill Version(s): <br>
1.1.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
