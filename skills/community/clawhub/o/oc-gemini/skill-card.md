## Description:

Use Gemini CLI for one-shot prompts, summaries, content generation, and managing skills, hooks, MCP, or Gemma routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run one-shot Gemini CLI prompts, summarize provided text, generate requested output, and manage Gemini extensions, skills, hooks, and MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Piped local file contents may be sent to the configured Gemini service.

Mitigation: Review or redact private content before piping files into Gemini.

## Reference(s):

- [Gemini API documentation](https://ai.google.dev/)
- [Gemini ClawHub release](https://clawhub.ai/hillstreet-ph/skills/oc-gemini)
- [Publisher profile](https://clawhub.ai/user/hillstreet-ph)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Code]

**Output Format:** [Gemini CLI response text, optionally JSON with --output-format json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response content and format follow the prompt.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
