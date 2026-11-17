## Description:

Deep multi-source research via Parallel API. Use when user explicitly asks for thorough research, comprehensive analysis, or investigation of a topic. For quick lookups or news, use parallel-search instead.

This skill is ready for commercial/non-commercial use.

## Publisher:

[normallygaussian](https://clawhub.ai/user/normallygaussian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to run deep multi-source research, competitive analysis, market research, due diligence, and other investigations where synthesized findings and source citations matter more than speed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research questions and input files may be sent to Parallel's service.

Mitigation: Avoid including secrets, confidential material, or regulated data unless the user's data-handling policy permits that external service use.

Risk: Saved research reports may remain on disk.

Mitigation: Choose output paths deliberately and remove generated report files when they are no longer needed.

Risk: The skill depends on an installed and authenticated Parallel CLI.

Mitigation: Verify CLI installation and authentication before use, and follow the official Parallel CLI integration documentation if setup fails.

## Reference(s):

- [Parallel](https://parallel.ai)
- [Parallel CLI Integration Docs](https://docs.parallel.ai/integrations/cli)
- [Parallel API Docs](https://docs.parallel.ai)
- [Parallel Research API Reference](https://docs.parallel.ai/api-reference/research)
- [ClawHub Skill Page](https://clawhub.ai/normallygaussian/skills/parallel-deep-research)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and expected JSON or Markdown research reports from the Parallel CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local JSON and Markdown report files when the agent runs Parallel CLI commands with an output path.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
