## Description: <br>
Memos Search lets an agent use a MemOS REST API to save, read, list, search, and delete persistent memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hope7709](https://clawhub.ai/user/hope7709) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill when they want an agent to rely on a MemOS server for persistent memory operations, including searching relevant memories and managing memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad persistent-memory read, write, search, list, and delete authority. <br>
Mitigation: Use it only with a trusted local or controlled MemOS server and require explicit user confirmation before saving or deleting memories. <br>
Risk: Stored memories may contain secrets or sensitive data that persist beyond the current session. <br>
Mitigation: Avoid storing secrets or sensitive data unless the server retention and access controls are understood and appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hope7709/memos-search) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API Calls, Configuration] <br>
**Output Format:** [Markdown instructions with REST endpoint descriptions and Python requests examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEMOS_API_URL for the target MemOS server; search examples use top_k up to 3.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
