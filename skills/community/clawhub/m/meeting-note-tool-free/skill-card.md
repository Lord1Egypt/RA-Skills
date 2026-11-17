## Description: <br>
会议纪要基础版 helps an agent turn meeting recordings or transcripts into structured meeting notes with basic information, topic analysis, decisions, consensus and disagreement points, action items, and Zettelkasten-style links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual users and lightweight teams use this skill to summarize discussion and decision meetings, extract conclusions and action items, and organize follow-up knowledge links. It is intended for meeting-management workflows where a user provides meeting text, recordings, or discussion notes to an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to use broad local file and command access while processing meeting material. <br>
Mitigation: Run it in a constrained workspace, review commands before execution, and limit file access to the meeting inputs and intended output directory. <br>
Risk: Meeting transcripts may contain confidential or personal information, and the artifact gives inconsistent local-only versus network/API guidance. <br>
Mitigation: Disable or explicitly approve network use before processing confidential meetings, and confirm where outputs, cache files, callback URLs, and API credentials are stored. <br>
Risk: The artifact suggests inspecting environment-variable names related to API keys, tokens, and secrets. <br>
Mitigation: Avoid exposing credential values, redact logs, and provide only the minimum API credentials needed for the selected agent environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/meeting-note-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Structured meeting notes or JSON-like responses with execution logs; may include Markdown and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill describes optional json, text, and csv output formats and a free-tier single-task workflow.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact/SKILL.md states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
