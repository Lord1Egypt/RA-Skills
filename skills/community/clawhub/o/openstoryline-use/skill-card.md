## Description: <br>
Runs an already installed OpenStoryline setup by starting local MCP and Web services, managing editing sessions, sending editing instructions, supporting re-edits, and verifying rendered video outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Anlittledy](https://clawhub.ai/user/Anlittledy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run OpenStoryline video-editing sessions after installation, provide editing prompts, continue work in an existing session, and confirm that new MP4 outputs were produced. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Feishu sender can upload a local file using stored OpenClaw credentials. <br>
Mitigation: Use the sender only when Feishu delivery is needed; verify the exact file path and recipient before sending, keep uploads limited to generated video outputs, and use least-privilege credentials. <br>
Risk: OpenStoryline configuration requires model, endpoint, and API-key values. <br>
Mitigation: Avoid committing config.toml or other files containing API keys, and review configuration changes before running the editing workflow. <br>
Risk: Local MCP and Web services could be exposed beyond the local machine if bound broadly. <br>
Mitigation: Keep services bound to 127.0.0.1 unless local-network access is explicitly required, and stop local services when finished. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Anlittledy/openstoryline-use) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes session identifiers and generated MP4 file paths when editing succeeds.] <br>

## Skill Version(s): <br>
0.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
