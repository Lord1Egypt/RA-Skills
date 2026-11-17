## Description: <br>
Four-layer memory system plugin for OpenClaw that captures conversations, extracts structured memories, summarizes scenes, and builds a user persona with local SQLite and Tencent Cloud VectorDB storage options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add long-term conversational memory to OpenClaw or Hermes agents, including automatic recall, structured memory extraction, scene summaries, persona generation, and migration or export tooling for memory stores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify OpenClaw behavior through high-impact host patching. <br>
Mitigation: Review or disable the postinstall patch path before installing in production environments. <br>
Risk: The skill captures and stores long-term conversation memory, which may include sensitive user or tool content. <br>
Mitigation: Deploy only where long-term memory capture is intended, configure retention carefully, and restrict access to local and remote memory stores. <br>
Risk: Optional backend offload and tracing can send conversations or tool payloads to external services. <br>
Mitigation: Use backend/offload and Opik or full-content tracing only with trusted endpoints and explicit operator approval. <br>
Risk: Insecure HTTPS settings or implicit user identification can weaken privacy controls. <br>
Mitigation: Do not use insecure HTTPS settings for sensitive data and set an explicit userId instead of relying on IP fallback. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/paudyyin/memory-tencentdb) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [OpenClaw host framework](https://github.com/nicepkg/openclaw) <br>
- [SQLite vector extension](https://github.com/asg017/sqlite-vec) <br>
- [node-llama-cpp](https://github.com/withcatai/node-llama-cpp) <br>
- [Tencent model API endpoint](https://api.lkeap.cloud.tencent.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and configuration snippets with command-line examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent memory records, scene Markdown, persona Markdown, search tool responses, and operational commands or configuration guidance.] <br>

## Skill Version(s): <br>
0.3.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
