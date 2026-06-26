## Description: <br>
Enables AI agents to develop evolving personas through organic memory growth, self-reflection, and layered memory management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zfanmy](https://clawhub.ai/user/zfanmy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to run a local memory and persona service that stores memories, searches them semantically, and generates or evolves agent persona profiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local memory server can retain private conversation content and persona inferences long term. <br>
Mitigation: Bind the service to localhost or add authentication before use, avoid storing secrets, and define retention rules for stored memories and persona data. <br>
Risk: The advertised delete endpoint does not actually erase memories. <br>
Mitigation: Do not rely on the delete endpoint for privacy guarantees until deletion is implemented and verified across Redis, SQLite, file, vector, and archive storage. <br>
Risk: Authentication and archival safeguards are weak for a service that stores sensitive memory data. <br>
Mitigation: Restrict network exposure, review backup and archive paths, and deploy only in environments where access controls and data handling are acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zfanmy/memprocessor) <br>
- [README](artifact/README.md) <br>
- [Privacy and Project Notice](artifact/VERSION-ISOLATION.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, API responses, Guidance] <br>
**Output Format:** [Python and FastAPI service files, JSON API responses, Markdown documentation, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local memory and persona service with REST endpoints for memory storage, search, analysis, and persona generation.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
