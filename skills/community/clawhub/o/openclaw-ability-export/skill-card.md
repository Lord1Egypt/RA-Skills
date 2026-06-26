## Description: <br>
Exports and imports OpenClaw agent configuration as a shareable Markdown bundle in chat, with selective import, merge rules, and privacy reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aitowerofbabel-lang](https://clawhub.ai/user/aitowerofbabel-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to share, back up, or transfer OpenClaw agent configuration through a Markdown ability package. It supports previewing imported content and choosing which of the supported configuration files to write. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exported configuration may include sensitive details from MEMORY.md, IDENTITY.md, TOOLS.md, or AGENTS.md. <br>
Mitigation: Review and redact the generated Markdown ability package before sharing it. <br>
Risk: Importing an ability package can overwrite selected workspace configuration files. <br>
Mitigation: Preview the package, import only trusted content, and confirm exactly which files should be written. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aitowerofbabel-lang/openclaw-ability-export) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/aitowerofbabel-lang) <br>
- [Skill homepage](https://clawic.com/skills/openclaw-ability-export) <br>
- [English README](artifact/README.md) <br>
- [Chinese README](artifact/README_zh.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown ability package and chat guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or write AGENTS.md, SOUL.md, TOOLS.md, IDENTITY.md, and MEMORY.md in the workspace root when the user chooses export or import.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
