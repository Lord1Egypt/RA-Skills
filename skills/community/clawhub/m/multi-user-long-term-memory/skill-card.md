## Description: <br>
Creates and manages isolated long-term Markdown memory files for multiple users so an agent can retain preferences and context across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kadbbz](https://clawhub.ai/user/kadbbz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when a multi-user chat or agent needs separate persistent memory per user across sessions. It is useful for retaining user preferences, context, and important notes without mixing memory between user identifiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory files may contain private user data if sensitive information is stored. <br>
Mitigation: Avoid storing secrets, credentials, regulated personal data, or information users have not agreed to retain, and periodically review or delete files in the users directory. <br>
Risk: Different sessions that share the same sender_id prefix will share the same memory file. <br>
Mitigation: Confirm the sender_id naming scheme separates users correctly before using the skill in shared or multi-tenant environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kadbbz/multi-user-long-term-memory) <br>
- [README.md](artifact/README.md) <br>
- [user-memory.js](artifact/references/user-memory.js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Code] <br>
**Output Format:** [Markdown memory files and plain-text CLI or module responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Memory is stored in per-user Markdown files keyed by the sanitized sender_id prefix before the pipe character.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
