## Description: <br>
Enhances OpenClaw agents with real-time Ollama streaming, Markdown tool-call recovery, and support for additional reasoning models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wd041216-bit](https://clawhub.ai/user/wd041216-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent engineers use this release to patch OpenClaw's Ollama provider for incremental streaming, fallback parsing of Markdown-embedded tool calls, and broader reasoning-model defaults. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release replaces core OpenClaw agent files rather than installing as an isolated skill. <br>
Mitigation: Apply it only to a backed-up or separate OpenClaw checkout after reviewing the diff and confirming compatibility with the target OpenClaw version. <br>
Risk: Markdown content from a model can be converted into executable tool calls. <br>
Mitigation: Use trusted models and prompts, keep tool permissions least-privileged, and review the Markdown-to-tool-call behavior before enabling it in sensitive workflows. <br>
Risk: Prompts and configured headers may be sent to the selected Ollama endpoint. <br>
Mitigation: Verify the Ollama endpoint and header configuration before use, especially when connecting to remote or shared services. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wd041216-bit/manusilized) <br>
- [Artifact skill overview](SKILL.md) <br>
- [Patch application notes](patches/README.md) <br>
- [Artifact-declared repository](https://github.com/manusilized/manusilized) <br>
- [Artifact-declared OpenClaw PRs link](https://github.com/openclaw/openclaw/pulls) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript patch files and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces manual patch instructions and replacement OpenClaw agent files rather than a standalone skill folder.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
