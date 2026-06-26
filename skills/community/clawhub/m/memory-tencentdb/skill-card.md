## Description: <br>
Memory TencentDB is an OpenClaw plugin that captures conversations and turns them into long-term memory, scene summaries, and persona context using SQLite or Tencent Cloud VectorDB backends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add long-term memory to OpenClaw agents, including automatic conversation capture, memory extraction, scene summarization, persona generation, and recall. It is intended for deployments that need either local SQLite storage or Tencent Cloud VectorDB-backed search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can capture conversation content and retain memory records. <br>
Mitigation: Enable it only for agents and workspaces where long-term memory is intended, and configure retention and excluded agents before deployment. <br>
Risk: The release can modify OpenClaw configuration or runtime files and start a sidecar process. <br>
Mitigation: Review install and patch scripts before installation, disable postinstall behavior where possible, and test in a controlled environment first. <br>
Risk: Optional remote model, database, tracing, or offload services may receive sensitive data. <br>
Mitigation: Keep offload and tracing disabled unless needed, use scoped credentials, and verify endpoint configuration before enabling remote backends. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/paudyyin/memory-tencentdb) <br>
- [Publisher Profile](https://clawhub.ai/user/paudyyin) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [sqlite-vec](https://github.com/asg017/sqlite-vec) <br>
- [node-llama-cpp](https://github.com/withcatai/node-llama-cpp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON configuration, shell commands, generated memory records, scene markdown, persona markdown, and optional HTML visualization] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing recall context and operational artifacts for OpenClaw memory workflows.] <br>

## Skill Version(s): <br>
0.3.8 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
