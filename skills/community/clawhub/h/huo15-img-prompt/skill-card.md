## Description:

Huo15 Img Prompt helps agents generate, refine, review, and package text-to-image, text-to-video, storyboard, brand-kit, and style-learning prompts for Midjourney, SD/SDXL, Flux, DALL-E 3, Sora, Kling, and related creative workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT

## Use Case:

Developers, designers, and creative teams use this skill to turn briefs, subjects, scripts, reference styles, and brand constraints into reusable prompts, prompt variants, storyboards, character assets, and creative production guidance for image and video generation tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can call paid external model APIs and send prompts, images, local files, or API-key-backed requests to network services.

Mitigation: Configure only trusted API providers, keep credentials scoped to the intended services, and review generated commands before running workflows that upload files or call external APIs.

Risk: The MCP server exposes creative tools to an agent and can broaden what the agent may execute in a session.

Mitigation: Register the MCP server only in trusted local agent environments and avoid shared or untrusted workspaces.

Risk: The image review workflow can operate on arbitrary local paths.

Mitigation: Use review_image only with intended non-sensitive image files and avoid passing private directories or unrelated file paths.

Risk: The Web UI and persisted character or project data may contain sensitive creative or brand material.

Mitigation: Run the Web UI only on loopback and avoid storing sensitive character, brand, or prompt data unless local persistence is acceptable.

Risk: A custom ANTHROPIC_BASE_URL can redirect model traffic through an unintended gateway.

Mitigation: Leave ANTHROPIC_BASE_URL unset unless it points to a trusted HTTPS endpoint.

## Reference(s):

- [Huo15 Img Prompt ClawHub page](https://clawhub.ai/zhaobod1/skills/huo15-img-prompt)
- [Quickstart](artifact/QUICKSTART.md)
- [Recipes](artifact/RECIPES.md)
- [T2I prompt engineering guide](artifact/references/t2i-guide.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with prompt text, JSON payloads, configuration snippets, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist project assets under ~/.huo15 and may generate files such as storyboards, scene prompts, transition prompts, brand kits, character cards, and learned presets.]

## Skill Version(s):

3.2.0 (source: frontmatter, changelog, server release metadata, artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
