## Description: <br>
Applies hersona character persona attributes to an agent session, including single-session, blended, persistent, reset, scoring, recommendation, creation, and export workflows backed by the hersona CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shiro-0x](https://clawhub.ai/user/shiro-0x) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to apply, inspect, blend, persist, reset, measure, recommend, create, and export generic hersona persona attributes for conversational sessions and downstream agent frameworks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent and reset commands can affect future sessions by writing SOUL.md or changing Hermes persona state. <br>
Mitigation: Prefer single or multi mode for session-only behavior, and review persistent and reset commands before use. <br>
Risk: Persistent persona setup can conflict with existing Hermes configuration or require manual config edits. <br>
Mitigation: Back up and validate config.yaml before applying persistent persona changes, and avoid automatic nested YAML writes. <br>
Risk: Persona memory input may introduce unwanted markdown-like content or exceed accepted size limits. <br>
Mitigation: Keep memory values within documented limits and rely on the skill's safelist escaping for markdown-sensitive characters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shiro-0x/skills/hersona) <br>
- [Publisher Profile](https://clawhub.ai/user/shiro-0x) <br>
- [Server-Resolved GitHub Import](https://github.com/shiro-0x/hersona/tree/main/skills/hersona) <br>
- [Project Homepage](https://github.com/shiro-0x/hersona) <br>
- [REFERENCE.md](artifact/REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with CLI command examples, system-prompt material, JSON-compatible export formats, configuration snippets, and operational guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce persona prompt material, hersona CLI commands, SOUL.md content, config.yaml snippets, validation checklists, and export payloads for supported agent frameworks.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
