## Description: <br>
Smart Memory gives OpenClaw agents persistent local JSON memory for storing, retrieving, updating, and maintaining user preferences, facts, decisions, instructions, dates, and technical context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcools1977](https://clawhub.ai/user/jcools1977) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to preserve relevant local context across conversations so agents can personalize responses and avoid asking for repeated facts or decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically store broad personal and technical information, including sensitive data, in long-term local memory. <br>
Mitigation: Use it only when persistent memory is intended, and do not store API keys, passwords, private server details, regulated personal data, or information that must be erased immediately. <br>
Risk: Forget and archive behavior may leave information retained after a user expects it to be removed. <br>
Mitigation: Use purge or hard-delete controls for erasure requests, and require explicit approval before storing sensitive or high-impact information. <br>
Risk: Memory export, search, and reporting commands can disclose stored memory content through local command output. <br>
Mitigation: Restrict access to the local memory directory and review command output before sharing logs, transcripts, or terminal captures. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jcools1977/openjaw-smart-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and local JSON memory records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local files under ~/.openclaw/smart-memory and shell scripts that require jq.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
