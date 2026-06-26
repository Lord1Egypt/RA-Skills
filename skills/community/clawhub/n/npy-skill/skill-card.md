## Description: <br>
Npy helps users create personalized AI companion persona skills from guided descriptions, personality matching, or authorized chat imports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwwttlll](https://clawhub.ai/user/wwwttlll) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Npy to generate and manage AI companion persona skills with relationship context, interaction modes, and versioned local files. The chat-import workflow is intended for authorized, consented personal data only. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can recover WeChat database keys and decrypt or parse local WeChat, iMessage, and text chat histories. <br>
Mitigation: Use sanitized plaintext exports where possible, import only data the user is authorized to use, and delete decrypted databases after the workflow is complete. <br>
Risk: The skill infers relationship traits and companion behavior from highly personal conversation data. <br>
Mitigation: Avoid importing conversations involving other people without consent, and review generated persona content before use. <br>
Risk: The skill can write persistent local skill files, relationship memory, versions, and global links. <br>
Mitigation: Review generated files and links before deployment, and remove unused persona data when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wwwttlll/npy-skill) <br>
- [README](artifact/README.md) <br>
- [Product requirements](artifact/docs/PRD.md) <br>
- [Intake prompt](artifact/prompts/intake.md) <br>
- [Smart matching prompt](artifact/prompts/smart_matching.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local persona skill files and related configuration when invoked by the user.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
