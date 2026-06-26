## Description: <br>
Clone and learn from a well-trained OpenClaw instance by extracting skills, memory, configuration, and expert knowledge from a source instance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhmza](https://clawhub.ai/user/zhmza) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to import or learn from another OpenClaw setup, including trusted backups, skill directories, expert profiles, memory, and persona files. It is intended for controlled migration and customization rather than blind copying. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can permanently import another person's skills, memory, persona files, and configuration into the user's OpenClaw workspace. <br>
Mitigation: Use only backups and profiles that the user controls or trusts, review every imported file before activation, and keep a restorable backup of the current workspace. <br>
Risk: Imported MEMORY.md, SOUL.md, expert files, and configs may contain secrets, personal data, or private context. <br>
Mitigation: Remove API keys, tokens, private memories, and other personal data before copying or activating imported files. <br>
Risk: Non-interactive imports from unknown archives reduce review opportunities before workspace changes occur. <br>
Mitigation: Avoid non-interactive imports from unknown archives; inspect archive contents and imported skill behavior first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhmza/openclaw-clone) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [TEST-REPORT.md](artifact/TEST-REPORT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash and YAML code blocks, plus an optional shell script workflow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include interactive prompts, non-interactive command examples, file-copy operations, and configuration snippets for an OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
