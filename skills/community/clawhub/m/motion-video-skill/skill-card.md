## Description:

Generates structured explainer animation videos from text, scripts, or Markdown, with narration-driven timing, web preview editing, optional TTS, and MP4 export only after explicit confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mr-q526](https://clawhub.ai/user/mr-q526)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, educators, product teams, and developers use this skill to turn written material into editable animated explainer video projects with synchronized narration timing, preview HTML, optional voice audio, and confirmed MP4 export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted movie.json project content may write outside the project or run script in generated previews.

Mitigation: Use trusted project files only, keep projects in a controlled workspace, and review generated previews before sharing or opening them in broader environments.

Risk: TTS and export commands perform local file-writing operations and may use external voice providers.

Mitigation: Avoid placing secrets in projects or chat, configure provider credentials outside project files, and run TTS or export commands only after explicit user confirmation.

Risk: Installing dependencies or browser components from an untrusted source can change the local execution environment.

Mitigation: Review the skill before installing, prefer a trusted npm registry, and install only the required Node.js, Playwright Chromium, and ffmpeg components for the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mr-q526/skills/motion-video-skill)
- [Publisher profile](https://clawhub.ai/user/mr-q526)
- [Movie Schema](references/movie-schema.md)
- [Animation Rules](references/animation-rules.md)
- [Prompt Patterns](references/prompt-patterns.md)
- [Template Catalog](references/template-catalog.md)
- [TTS Catalog](references/tts-catalog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands plus JSON movie project files, preview HTML, optional audio tracks, and confirmed MP4 export.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; MP4 export also requires Playwright Chromium and ffmpeg. Cloud TTS requires user-provided provider credentials and explicit voice confirmation.]

## Skill Version(s):

1.0.0 (source: release evidence; artifact package.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
