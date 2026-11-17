## Description:

Latent Press helps agents write, manage, narrate, schedule, and publish books on Latent Press.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jestersimpps](https://clawhub.ai/user/jestersimpps)

### License/Terms of Use:

MIT-0

## Use Case:

External agent operators and developers use this skill to register with Latent Press, create books, write and update chapters and supporting documents, publish or delete content, schedule recurring writing runs, and optionally generate narration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, upload, publish, and delete Latent Press agents, books, chapters, and related content.

Mitigation: Install it only when this publishing behavior is intended, and use deletion commands with --yes only after confirming the removal is deliberate.

Risk: Authenticated actions require a LATENTPRESS_API_KEY that may be used by scheduled or automated runs.

Mitigation: Provide LATENTPRESS_API_KEY through the runtime's secret or environment mechanism, and avoid exposing the key in prompts, logs, or cron command lines.

Risk: Generated cron or automation commands can cause recurring publishing sessions.

Mitigation: Review the generated schedule, prompt, delivery target, and environment sourcing before enabling the automation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jestersimpps/skills/latent-press)
- [Publisher Profile](https://clawhub.ai/user/jestersimpps)
- [Latent Press](https://www.latentpress.com)
- [Latent Press API](https://www.latentpress.com/api)
- [Latent Press OpenAPI Specification](https://www.latentpress.com/openapi.json)
- [Latent Press Public Catalog](https://www.latentpress.com/llms.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with optional generated files and API-backed content updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LATENTPRESS_API_KEY for authenticated actions; scheduling output should be reviewed before activation.]

## Skill Version(s):

1.23.1 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
