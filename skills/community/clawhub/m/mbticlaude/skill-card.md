## Description:

Infers MBTI personality types by analyzing user prompts across Claude Code, Codex, Gemini, OpenCode, and OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xmanrui](https://clawhub.ai/user/xmanrui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI tool users use this skill to analyze local prompt histories and receive an MBTI-style personality inference with dimension-level notes and caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local AI prompt histories that may contain secrets, code, personal notes, or business data.

Mitigation: Review the release before installation, use a pinned version, and limit or clean local history files before running it.

Risk: MBTI inference from work prompts can be misleading and is not a professional psychological assessment.

Mitigation: Use the output as informal guidance only and avoid employment, medical, or other consequential decisions.

Risk: Low or unrepresentative prompt history can reduce analysis quality.

Mitigation: Run the skill only when there is sufficient relevant history and treat sparse-data results as inconclusive.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xmanrui/skills/mbticlaude)
- [ClawHub Publisher Profile](https://clawhub.ai/user/xmanrui)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an MBTI type estimate, dimension-level analysis, data-count summary, and cautionary notes.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
