## Description: <br>
Transform into 20 specialized AI personalities on demand. Switch mid-conversation and load only the active persona. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to switch an agent among bundled personas for coding, writing, learning, lifestyle, and professional-orientation tasks while loading only the active persona. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The selected persona can persist across sessions through local active-persona state. <br>
Mitigation: Use /persona exit, scripts/persona.py --reset, or an equivalent reset before switching contexts where the prior persona should not apply. <br>
Risk: Medical, legal, fitness, career, or security personas can be mistaken for professional advice. <br>
Mitigation: Treat those personas as general educational or orientation guidance and consult qualified professionals for decisions in regulated or high-impact domains. <br>
Risk: Persona prompts can change the agent's tone and priorities in ways that are inappropriate for a later task. <br>
Mitigation: Use explicit /persona commands and confirm or reset the active persona before starting sensitive, formal, or unrelated work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/robbyczgw-cla/personas) <br>
- [README.md](README.md) <br>
- [FAQ.md](FAQ.md) <br>
- [OVERVIEW.md](OVERVIEW.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown persona prompts and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Loads one active persona at a time; local active-persona state may persist in ~/.openclaw/persona-state.json.] <br>

## Skill Version(s): <br>
2.2.6 (source: SKILL.md frontmatter, skill.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
