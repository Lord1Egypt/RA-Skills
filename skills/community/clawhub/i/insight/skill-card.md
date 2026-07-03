## Description: <br>
25-perspective universal AI note analysis. Multi-source: Obsidian/Flomo/Evernote/Dedao/markdown. Auto-detect note type + time range filtering + persona integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pigro0314](https://clawhub.ai/user/pigro0314) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to analyze personal or work notes through multiple thinking frameworks, time filters, source filters, and optional persona lenses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to read broad sets of private notes, including journals, health notes, relationship details, and third-party information. <br>
Mitigation: Scope note directories and sources narrowly, avoid `--source all` unless necessary, and use the skill only with notes you are comfortable sending through the active agent and model stack. <br>
Risk: The default output mode can modify notes by appending analysis markers and generated content. <br>
Mitigation: Prefer `--output reply-only` for review-first use, or `--output separate` when keeping generated analysis outside the original notes is important. <br>
Risk: Some perspectives infer mental health, personality, relationship, or motivation patterns from personal writing. <br>
Mitigation: Treat outputs as reflective prompts rather than diagnosis or professional advice, and avoid running those perspectives on sensitive notes without explicit user intent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pigro0314/insight) <br>
- [Artifact README](README.md) <br>
- [Artifact skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown analysis returned in chat, appended to source notes, or written as a separate markdown file depending on output mode.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports source, search, time range, note type, perspective, persona, directory, glob, output mode, and note count parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
