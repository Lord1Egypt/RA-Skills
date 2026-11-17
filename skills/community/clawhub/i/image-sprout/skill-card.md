## Description:

Image Sprout helps agents generate and iterate on repeatable images using saved project context, reference images, style guides, and subject guides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmchow](https://clawhub.ai/user/tmchow)

### License/Terms of Use:


## Use Case:

Developers, creators, and agents use this skill to operate Image Sprout projects, derive reusable style and subject guides from reference images, and generate consistent image outputs for downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Image Sprout web UI has no authentication and could expose local project data if published on the public internet.

Mitigation: Keep the web UI on localhost or a private network, and do not expose it publicly.

Risk: Reference images, generated outputs, project instructions, and the OpenRouter API key are stored locally by the Image Sprout tool.

Mitigation: Use trusted machines and accounts, protect the local app data directory, and verify that local storage is acceptable before use.

Risk: Concurrent agents can collide if they rely on Image Sprout's shared current-project state.

Mitigation: Pass the project explicitly with --project in agent workflows.

## Reference(s):

- [Image Sprout GitHub Repository](https://github.com/tmchow/image-sprout)
- [Image Sprout ClawHub Skill Page](https://clawhub.ai/tmchow/skills/image-sprout)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with inline shell commands and JSON-output usage patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to request structured CLI JSON output and extract generated image paths for downstream tools.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
