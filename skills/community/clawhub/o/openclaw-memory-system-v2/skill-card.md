## Description: <br>
OpenClaw 记忆管理系统 uses NOW.md, daily logs, and a structured knowledge base to help agents persist, organize, verify, and retire local memory across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muisenice](https://clawhub.ai/user/muisenice) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to set up file-based local memory so an agent can track current state, append daily events, consolidate reusable knowledge, verify updates, and archive stale context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory may capture secrets, personal data, or topics that should not survive across sessions. <br>
Mitigation: Set explicit rules for what may be saved, which topics are excluded, how entries are reviewed, and how memory can be deleted or restored before enabling the workflow. <br>
Risk: Repeated saving and reorganization can make inaccurate, conflicting, or stale memories appear authoritative. <br>
Mitigation: Use the documented read-compare-update flow, mark conflicts or superseded entries, and periodically review or archive stale memory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/muisenice/openclaw-memory-system-v2) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with file paths, tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory-management instructions; no API calls or credential variables are declared.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact heading says v1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
