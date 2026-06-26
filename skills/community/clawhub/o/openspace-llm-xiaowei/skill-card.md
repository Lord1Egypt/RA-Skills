## Description: <br>
Adapts HKUDS OpenSpace into an OpenClaw-callable skill for MiniMax-M2.7 chat, writing, text analysis, and code generation with proxy, timeout, and retry configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linhuiguo](https://clawhub.ai/user/linhuiguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to call a MiniMax-backed OpenSpace LLM workflow from the command line or Python for conversation, long-form writing, text analysis, and code generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The README publishes a full-looking MiniMax API key. <br>
Mitigation: Treat the published key as exposed and unsafe, do not use it, and configure a fresh MiniMax credential through a secure environment variable or secret manager. <br>
Risk: Prompts and generated work are sent to an external LLM service. <br>
Mitigation: Avoid sending secrets, private files, regulated data, or proprietary text unless the external provider, account, and retention settings are approved for that data. <br>
Risk: Runtime behavior depends on the openspace dependency and local proxy configuration. <br>
Mitigation: Verify the openspace package source and version, review proxy settings, and test the connection in a controlled environment before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/linhuiguo/openspace-llm-xiaowei) <br>
- [HKUDS OpenSpace project](https://github.com/HKUDS/OpenSpace) <br>
- [MiniMax API endpoint](https://api.minimax.chat/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Command-line or Python string output, including generated prose, analysis, and code blocks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses depend on the configured MiniMax/OpenSpace model, API key, proxy, timeout, and retry settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
