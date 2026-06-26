## Description: <br>
Create, edit, improve, tidy, review, audit, or restructure OpenClaw AgentSkills and SKILL.md files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haseo-ai](https://clawhub.ai/user/haseo-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to create, improve, audit, and maintain OpenClaw AgentSkills with clear triggering metadata, style guidance, workflow phases, and validation examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated skill edits could introduce incorrect or misleading guidance into persistent workspace skills. <br>
Mitigation: Review generated SKILL.md changes and run a skill audit before keeping or deploying them. <br>
Risk: Sub-agent prompts or generated examples could include secrets or unrelated private workspace context if that context is supplied to the skill. <br>
Mitigation: Avoid passing secrets or unrelated private workspace context into generated sub-agent prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haseo-ai/oc-skill-creator) <br>
- [OpenClaw vs Codex Skill Creator](references/openclaw-vs-codex.md) <br>
- [OpenClaw vs Codex Skill Creator (Japanese)](references/openclaw-vs-codex.ja.md) <br>
- [OpenClaw vs Codex Skill Creator (Korean)](references/openclaw-vs-codex.ko.md) <br>
- [OpenClaw vs Codex Skill Creator (Chinese)](references/openclaw-vs-codex.zh.md) <br>
- [Summarize validation example](examples/summarize.md) <br>
- [Changelog validation example](examples/changelog.md) <br>
- [Scaffold validation example](examples/scaffold.md) <br>
- [Screenshot-capture validation example](examples/screenshot-capture.md) <br>
- [Unit-converter validation example](examples/unit-converter.md) <br>
- [Skill-audit validation example](examples/skill-audit.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with SKILL.md examples and file-organization recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or edit persistent workspace skills; generated edits should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
