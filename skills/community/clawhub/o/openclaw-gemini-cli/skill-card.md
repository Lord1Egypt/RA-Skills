## Description: <br>
Use the local Gemini CLI for one-shot prompts, structured JSON output, shell-assisted research, and delegated AI-to-AI workflows while keeping command execution and file edits under the primary agent's control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hiromps](https://clawhub.ai/user/hiromps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to invoke an installed Gemini CLI for quick secondary opinions, JSON-only responses, code or content drafting, and bounded file reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: File-review workflows can send selected file contents to Gemini, which may expose secrets, credentials, private source code, or personal data. <br>
Mitigation: Install and authenticate the official Gemini CLI yourself, verify the expected binary with `which gemini`, and avoid using the review helper on sensitive files or data. <br>
Risk: Gemini output may contain incorrect guidance, unsafe shell commands, or edits that need human or agent review before use. <br>
Mitigation: Treat Gemini responses as advice, review generated commands and edits before applying them, and run appropriate validation after changes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, plus optional text, JSON, or code returned by Gemini CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed and authenticated Gemini CLI; selected file-review inputs may be sent to Gemini.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
