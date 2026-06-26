## Description: <br>
Mema's personal brain - SQLite metadata index for documents and Redis short-term context buffer. Use for organizing workspace knowledge paths and managing ephemeral session state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1999AZZAR](https://clawhub.ai/user/1999AZZAR) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use Mema Brain to organize workspace knowledge paths in a local SQLite metadata index and pass short-lived session context through a configured Redis instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reference sensitive local paths in its memory index. <br>
Mitigation: Index only paths intended for agent memory and avoid adding sensitive workspace locations. <br>
Risk: Redis-backed short-term memory depends on the configured Redis instance. <br>
Mitigation: Point REDIS_HOST and REDIS_PORT only at a Redis instance the user controls or trusts. <br>
Risk: The mental clear workflow can erase the skill's Redis-backed memory state. <br>
Mitigation: Use clear operations deliberately and treat them as a full reset when no key is specified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1999AZZAR/mema) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; runtime commands print plain text status and query results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, redis Python package, REDIS_HOST, and REDIS_PORT; stores document metadata under ~/.openclaw/memory and short-term state in Redis with a default 6-hour TTL.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
