## Description: <br>
Generates platform-adapted photo captions for Instagram, X (Twitter), and Facebook from a user's photo description, location, camera details, subject, and mood. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal social media users and photography hobbyists use this skill to turn photo context into ready-to-post captions tailored to Instagram, X (Twitter), and Facebook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests read, write, and command execution permissions that are broader than its caption-writing behavior appears to need. <br>
Mitigation: Review permissions before installation, prefer a version with reduced permissions, or run it only where file and command access can be explicitly controlled. <br>
Risk: Photo prompts may include sensitive location, routine, family, or personal metadata. <br>
Mitigation: Avoid supplying exact home locations, routines, minors' details, or other sensitive identifiers when requesting captions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/photo-caption-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Source skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text captions grouped by social platform] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces separate caption styles for Instagram, X (Twitter), and Facebook; captions depend on the user's supplied photo details.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
