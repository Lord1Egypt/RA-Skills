## Description: <br>
Mental Health helps users with mood checks, breathing exercises, journaling prompts, mental-health resources, stress management, and gratitude practice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill for self-guided wellness check-ins, breathing exercises, journaling, stress-management suggestions, and pointers to mental-health resources. It is not a substitute for professional mental-health care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store wellness or mental-health entries in local plaintext files. <br>
Mitigation: Review storage paths before use, avoid entering highly sensitive or crisis details, and remove local data manually when retention is not desired. <br>
Risk: The reviewed reset behavior does not actually delete stored data. <br>
Mitigation: Do not rely on the advertised reset command for deletion; inspect and remove the relevant local files directly. <br>
Risk: Users may treat self-guided wellness output as professional mental-health care. <br>
Mitigation: Keep the disclaimer visible and direct users with severe distress, self-harm thoughts, or ongoing impairment to emergency or professional resources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/mental-health) <br>
- [Publisher profile](https://clawhub.ai/user/bytesagain-lab) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [Feedback and feature requests](https://bytesagain.com/feedback) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, files] <br>
**Output Format:** [Markdown and terminal text with shell command examples and local text log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append wellness or journal entries to local plaintext files depending on the invoked script and command.] <br>

## Skill Version(s): <br>
2.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
