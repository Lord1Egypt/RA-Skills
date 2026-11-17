## Description:

PaperView API helps agents generate ECharts visualizations, AI scientific diagrams, and word clouds from data, text, or PDF paper URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yyccr](https://clawhub.ai/user/yyccr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and external users use this skill to call PaperView APIs for charts, scientific diagrams, and word-cloud keyword extraction, then render or save the returned visual outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected chart data or public PDF URLs are sent to PaperView for processing.

Mitigation: Use the skill only with data and public PDF URLs approved for submission to PaperView.

Risk: Generated HTML can run remote scripts and embed API responses directly into executable browser code.

Mitigation: Treat generated HTML as untrusted output; harden it with safe JSON embedding, pinned dependencies, and integrity checks before using it with sensitive datasets.

Risk: The skill requires a PaperView API token.

Mitigation: Store the token in the PAPERVIEW_API_TOKEN environment variable and avoid exposing it in prompts, logs, generated files, or shared command history.

## Reference(s):

- [PaperView homepage](https://www.ipaperview.com)
- [PaperView API base URL](https://api.ipaperview.com)
- [ClawHub skill page](https://clawhub.ai/yyccr/skills/paper-view-skill)
- [Artifact-declared source repository](https://github.com/yyccR/paper-view-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON examples, curl commands, and self-contained HTML rendering code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API request guidance, ECharts option handling, Server-Sent Events parsing guidance, image URL handling, and browser-renderable HTML.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
