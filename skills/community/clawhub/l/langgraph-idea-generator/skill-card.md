## Description:

Generates a concise LangGraph-based coding plan from a short request, including a category, complexity estimate, command, scenario, and target file path while checking existing local script names to reduce duplicate work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colbertlee](https://clawhub.ai/user/colbertlee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to turn a brief coding idea into a small implementation plan with an executable command, scenario summary, and suggested script file path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the user's coding request to the external MiniMax model service.

Mitigation: Avoid submitting sensitive requests and use a dedicated API key for the service.

Risk: The skill may send up to 30 local Python script filenames from ~/.openclaw/workspace-coding-advisor/scripts to MiniMax.

Mitigation: Avoid sensitive filenames in that directory or review the directory contents before running the skill.

Risk: Rebuilding the bundled virtual environment without pinned dependencies can change runtime behavior.

Mitigation: Prefer pinned dependency installation when recreating the virtual environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/colbertlee/skills/langgraph-idea-generator)
- [MiniMax Anthropic-compatible API endpoint](https://api.minimaxi.com/anthropic)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Human-readable CLI text or JSON when IDEA_GEN_JSON=1]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans are constrained to three implementation lines and may include local script filename context.]

## Skill Version(s):

1.2.0 (source: server release metadata, skill.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
