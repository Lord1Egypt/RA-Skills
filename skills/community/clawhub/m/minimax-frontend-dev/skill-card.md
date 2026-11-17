## Description:

Builds complete frontend experiences with UI design, cinematic animation, AI-generated MiniMax media assets, persuasive copy, and generative art guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daidai8910g](https://clawhub.ai/user/daidai8910g)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and frontend engineers use this skill to build landing pages, marketing sites, product pages, dashboards, and rich web experiences that combine local media assets, motion, copywriting, and implementation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and prompts may be sent to a user-configured MiniMax endpoint.

Mitigation: Set MINIMAX_API_BASE only to official MiniMax HTTPS endpoints and use a narrowly scoped, revocable API key.

Risk: Generated image, video, or audio downloads may come from unvalidated URLs returned by the provider.

Mitigation: Treat downloaded media as untrusted until the URL, file type, and content are reviewed before publication or reuse.

Risk: Prompt text, lyrics, or narration sent to the media APIs may contain confidential or rights-sensitive material.

Mitigation: Avoid confidential inputs and verify rights for text, lyrics, voices, imagery, and generated assets before commercial use.

Risk: Dependency setup guidance uses unpinned package installation.

Mitigation: Install dependencies in a managed environment and pin package versions before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daidai8910g/skills/minimax-frontend-dev)
- [MiniMax provider reference](references/minimax-cli-reference.md)
- [Environment setup](references/env-setup.md)
- [Asset prompt guide](references/asset-prompt-guide.md)
- [MiniMax image guide](references/minimax-image-guide.md)
- [MiniMax video guide](references/minimax-video-guide.md)
- [MiniMax TTS guide](references/minimax-tts-guide.md)
- [MiniMax music guide](references/minimax-music-guide.md)
- [MiniMax voice catalog](references/minimax-voice-catalog.md)
- [Motion recipes](references/motion-recipes.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and generated project files or assets when used by an agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call MiniMax APIs through bundled scripts when MINIMAX_API_KEY and MINIMAX_API_BASE are configured.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
