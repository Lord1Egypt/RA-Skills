## Description:

InkOS helps agents operate a novel-writing CLI and local Studio workbench to plan, generate, audit, revise, import, and export long-form fiction with configurable LLM providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adchina2025](https://clawhub.ai/user/adchina2025)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, developers, and agent operators use this skill to create or continue novels, steer chapter focus, manage story state, audit generated prose, detect AI-generated passages, and export manuscripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and drives an unpinned third-party npm executable that may process manuscripts and API keys.

Mitigation: Verify the @actalk/inkos package and publisher before installation, pin an approved package version where possible, and run it only in trusted project workspaces.

Risk: Configured LLM provider endpoints receive prompts, manuscript context, and API credentials needed for generation.

Mitigation: Use scoped API keys, prefer environment-variable based key configuration, and point custom base URLs only at trusted or audited providers.

Risk: Project configuration, logs, and generated files may contain sensitive manuscript material or credentials.

Mitigation: Keep inkos.json, logs, and draft project directories out of source control unless reviewed and scrubbed.

Risk: Self-update behavior can change the executable after approval in managed environments.

Mitigation: Avoid self-update paths in managed deployments unless the updated package receives a fresh review.

## Reference(s):

- [InkOS GitHub Repository](https://github.com/Narcooo/inkos)
- [ClawHub Skill Page](https://clawhub.ai/adchina2025/skills/inkos-novel-writer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands, configuration notes, and structured JSON command options where supported]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to generate or manage local manuscript files, project configuration, exports, logs, and Studio sessions through the InkOS CLI.]

## Skill Version(s):

2.3.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
