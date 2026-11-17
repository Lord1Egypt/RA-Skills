## Description:

Huo15 Img Test helps agents create, refine, lint, reverse-engineer, and optionally render image and video generation prompts for Midjourney, Stable Diffusion, SDXL, Flux, DALL-E, and related tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn rough creative briefs into structured image or video prompts, produce model-specific prompt formats, inspect prompt metadata from reference images, and optionally call supported rendering backends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional polishing and rendering features can send prompts and API keys to external services.

Mitigation: Avoid these features for sensitive prompts, configure only trusted endpoints, and review credentials before use.

Risk: Changing the Anthropic base URL can route requests to an untrusted host.

Mitigation: Use the default or a verified endpoint and do not set ANTHROPIC_BASE_URL to an untrusted value.

Risk: Reference-image reverse prompting can fetch arbitrary URLs.

Mitigation: Avoid untrusted URLs or run URL-based analysis in a network-restricted environment.

Risk: Safety rewriting behavior may conflict with target platform policies.

Mitigation: Review rewritten prompts against the relevant platform policy before using them.

Risk: Broad auto-triggers may activate the toolkit for prompts that do not need network-backed or rendering behavior.

Mitigation: Confirm the intended script and options before running commands that fetch URLs or call external APIs.

## Reference(s):

- [T2I prompt engineering reference](artifact/references/t2i-guide.md)
- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-img-test)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, Markdown, JSON recipes, and shell commands depending on the invoked script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prompts, negative prompts, consistency locks, JSON metadata, platform warnings, and backend rendering instructions.]

## Skill Version(s):

2.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
