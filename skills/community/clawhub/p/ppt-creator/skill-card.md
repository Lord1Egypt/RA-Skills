## Description:

PPT Creator helps agents create, review, edit, restyle, and download presentation decks through Yoo AI from topics, structured outlines, local files, or project summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daan0701](https://clawhub.ai/user/daan0701)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation authors use this skill to turn prompts, outlines, files, and codebase summaries into PPT decks, then review outlines, preview covers, add speaker notes, insert slides, or regenerate with a different style before downloading the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send PPT content, local file contents, or project summaries to Yoo AI.

Mitigation: Use it only with content approved for that external service, and avoid sensitive or confidential source material unless sharing is authorized.

Risk: The skill needs a Yoo AI API key and can read a fallback key from config.json.

Mitigation: Prefer storing YOO_AI_API_KEY in a secure environment variable and avoid committing real credentials into config.json.

Risk: The documented command templates accept user-provided text, paths, JSON, and URLs.

Mitigation: Pass arguments with safe argument-array execution and review untrusted inputs before running commands.

Risk: The skill writes downloaded decks, outline JSON files, and task records to the local workspace.

Mitigation: Review the configured output directory and generated files before sharing or retaining them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daan0701/skills/ppt-creator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown and text guidance with shell commands, JSON outline files, status and editor URLs, and downloaded PPTX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Yoo AI API key; generated decks and task records are written locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
