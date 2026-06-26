## Description: <br>
Shared folder that automatically synchronizes between peers using Pilot Protocol pub/sub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and agents use this skill to maintain a persistent shared folder across peers with automatic file synchronization and eventual consistency. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Peer messages can automatically delete files or request files from the shared folder without enough containment. <br>
Mitigation: Use a dedicated non-sensitive folder, share only with trusted peers, require peer authorization before honoring pull or delete events, and add backups, versioning, or trash behavior for removals. <br>
Risk: Untrusted filenames in peer events can target paths outside the intended shared folder. <br>
Mitigation: Canonicalize filenames before use and reject slashes, parent-directory segments, and paths that resolve outside the shared folder. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilot-protocol, pilotctl, jq, a filesystem watcher, and a running Pilot daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
