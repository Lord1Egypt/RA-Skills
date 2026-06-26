## Description: <br>
Production memory for AI agents. Cloudflare-native with 99.1% LOCOMO accuracy. Knowledge graph, temporal reasoning, multi-hop retrieval. Free tier available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phillipneho](https://clawhub.ai/user/phillipneho) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and agent operators use Muninn Memory to add persistent semantic, episodic, and procedural memory to AI agents through MCP tools, with local SQLite/Ollama operation or a hosted cloud API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent memories can contain private or sensitive user data. <br>
Mitigation: Use local mode for private data, avoid storing secrets, and review memory retention and deletion behavior before deployment. <br>
Risk: Cloud and model-backed embedding modes can send memory content or queries to configured services. <br>
Mitigation: Verify environment variables and provider settings before use, and choose local Ollama processing when external processing is not acceptable. <br>
Risk: Persisted or stale memories can influence later agent responses. <br>
Mitigation: Use the forget, audit, integrity, and contradiction review capabilities to remove, verify, and reconcile stored memories. <br>


## Reference(s): <br>
- [ClawHub Muninn Memory Listing](https://clawhub.ai/phillipneho/muninn-skill) <br>
- [Muninn Cloud Dashboard](https://muninn.au) <br>
- [LOCOMO Benchmark Analysis](docs/LOCOMO_ANALYSIS.md) <br>
- [Muninn Enhancement Ideation](docs/ENHANCEMENT_IDEATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [MCP tool responses, Markdown guidance, JSON-like tool results, TypeScript code, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store and retrieve user or agent memory content; behavior depends on selected local or cloud embedding mode.] <br>

## Skill Version(s): <br>
2.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
