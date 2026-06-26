## Description: <br>
Prismer enables agents to fetch, compress, and parse web content, perform OCR, communicate through real-time messaging, and use shared memory and evolution workflows through the Prismer CLI and SDKs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ooxxxxoo](https://clawhub.ai/user/ooxxxxoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Prismer to give coding or assistant agents cloud-backed context loading, document parsing, messaging, tasks, memory, file sharing, and shared evolution feedback via the Prismer CLI and SDKs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants agents broad cloud upload, memory, messaging, and skill-install capabilities. <br>
Mitigation: Use a dedicated low-privilege Prismer account or key, and require explicit approval before uploading files, parsing confidential documents, sending or deleting messages, or recording task and error details. <br>
Risk: The workflow can install packages and synchronize skills from external services. <br>
Mitigation: Install only if Prismer Cloud and the referenced packages are trusted, and review any skill before installing or syncing it. <br>
Risk: API keys or other secrets could be exposed if passed directly through commands or shared logs. <br>
Mitigation: Avoid passing secrets directly on the command line and keep credentials in a scoped, revocable secret store. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ooxxxxoo/global-agent-node-with-real-time-context-streaming-mission-form-autonomous-network-status-awaiting-peers) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/ooxxxxoo) <br>
- [Prismer Cloud](https://prismer.cloud) <br>
- [Prismer Cloud Docs](https://prismer.cloud/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with CLI commands, SDK code examples, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include package installation commands, Prismer Cloud API usage, account registration, API keys, file uploads, memory writes, messaging actions, and skill installation or synchronization steps.] <br>

## Skill Version(s): <br>
1.7.4 (source: server release metadata and user changelog, released 2026-04-01) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
