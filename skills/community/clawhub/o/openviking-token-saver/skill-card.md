## Description: <br>
OpenViking Token Saver helps agents manage an OpenViking context database with layered L0/L1/L2 loading, semantic search, file-system memory, and token-use tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnoder-wgh](https://clawhub.ai/user/cnoder-wgh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install and operate OpenViking as a local context database, search project or knowledge-base content, browse layered summaries and full reads, and compare token consumption. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently ingest local or remote content into a local knowledge base. <br>
Mitigation: Add only intended directories or URLs, avoid broad paths such as home folders or full repositories with secrets, and review stored workspace content periodically. <br>
Risk: Setup can store model-provider API keys in local OpenViking configuration. <br>
Mitigation: Use restricted provider keys where possible and inspect permissions on ~/.openviking/ov.conf after configuration. <br>
Risk: Installer and setup scripts can modify the local environment. <br>
Mitigation: Review shell scripts before execution and run them in a controlled environment when evaluating the skill. <br>
Risk: Broad trigger phrases may cause the skill to activate for general search or project-inspection requests. <br>
Mitigation: Use product-specific prompts when invoking OpenViking and confirm the target resource before adding, searching, or reading content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cnoder-wgh/openviking-token-saver) <br>
- [OpenViking GitHub](https://github.com/volcengine/OpenViking) <br>
- [OpenViking website](https://www.openviking.ai) <br>
- [LiteLLM provider documentation](https://docs.litellm.ai/docs/providers) <br>
- [NVIDIA NIM API](https://build.nvidia.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local OpenViking configuration, workspace data, and token statistics.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
