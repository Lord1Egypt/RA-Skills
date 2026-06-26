## Description: <br>
Cognitive memory system for AI agents with an Atkinson-Shiffrin memory model, semantic RAG, trust scoring, and metacognitive error prevention. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wazionapps](https://clawhub.ai/user/wazionapps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use NEXO Brain to add persistent local memory, semantic retrieval, session continuity, mistake prevention, reminders, entity tracking, and preference memory to an AI agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable local memory may preserve user, project, entity, and preference history across agent sessions. <br>
Mitigation: Enable the skill only when persistent local memory is intended, and keep secrets or highly sensitive personal data out of captured sessions unless exclusion and deletion controls have been verified. <br>
Risk: The installed runtime appears broader than the skill page clearly discloses, including possible local indexing or background automation behavior. <br>
Mitigation: Review the npm package and project homepage behavior before enabling the runtime, and decide whether local file or email indexing and background automation are acceptable for the environment. <br>
Risk: The MCP server runs from a local Python entry point under the user's NEXO home directory and can affect agent memory and workflow behavior. <br>
Mitigation: Install from the expected `nexo-brain` package, review the generated OpenClaw MCP configuration, and restrict use to macOS or Linux environments where `python3` is available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wazionapps/skills/nexo-brain) <br>
- [Project homepage](https://github.com/wazionapps/nexo) <br>
- [NEXO Brain npm package](https://www.npmjs.com/package/nexo-brain) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes MCP server setup guidance for a local memory runtime on macOS and Linux.] <br>

## Skill Version(s): <br>
7.38.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
