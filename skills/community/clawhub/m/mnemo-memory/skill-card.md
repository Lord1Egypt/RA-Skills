## Description: <br>
Cloud-persistent memory for AI agents that uses TiDB Serverless for cross-session recall, multi-agent sharing, and hybrid vector plus keyword search across OpenClaw, Claude Code, and OpenCode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiffang](https://clawhub.ai/user/qiffang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and teams use mnemo-memory to give AI agents cloud-backed memory for cross-session recall, shared memory pools, and hybrid search through TiDB Cloud Serverless. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored memories and database credentials are sensitive because this skill uses a cloud-backed database and can share memory across configured agents or teammates. <br>
Mitigation: Use dedicated TiDB credentials, protect configuration files, restrict database and team access, and avoid storing secrets, regulated data, or private source material unless that use is approved. <br>
Risk: Shared or team memory modes can expose, modify, or delete memories across agents if access is too broad. <br>
Mitigation: Review who can access or delete memories, use per-agent tokens or isolated spaces where available, and test shared-memory behavior before production use. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/qiffang/mnemo-memory) <br>
- [GitHub repository](https://github.com/qiffang/mnemos) <br>
- [Design document](https://github.com/qiffang/mnemos/blob/main/docs/DESIGN.md) <br>
- [CRDT memory proposal](https://github.com/qiffang/mnemos/blob/main/claude-notes/crdt-memory-proposal.md) <br>
- [TiDB Cloud Serverless](https://tidbcloud.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe cloud memory setup, memory operations, and shared-agent behavior.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
