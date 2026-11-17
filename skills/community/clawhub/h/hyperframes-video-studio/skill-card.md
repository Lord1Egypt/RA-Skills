## Description:

Guided OpenClaw video studio for Hyperframes: templates, safety audit, local-first TTS, and renderable HTML projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to create template-based product, report, social, explainer, testimonial, event, changelog, and commerce videos from briefs and user-selected materials. It guides asset intake, narration, local environment checks, HTML project generation, and optional rendering with Hyperframes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read user-selected files and store excerpts and absolute paths in cache or project files.

Mitigation: Avoid broad or sensitive folders, review asset manifests and generated project files, and keep generated outputs private until reviewed.

Risk: Narration may use Edge-TTS, which is zero-cost and keyless but network-backed.

Mitigation: Use local Piper for confidential narration or skip TTS when local speech tooling is unavailable.

Risk: Hyperframes installation and CDN-loaded GSAP are third-party code paths without strong pinning.

Mitigation: Install only after review and confirmation, prefer local cache-scoped dependencies, and scan generated HTML before sharing or rendering.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tobewin/skills/hyperframes-video-studio)
- [Hyperframes Upstream Repository](https://github.com/heygen-com/hyperframes)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON command inputs, shell commands, and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates cache-scoped manifests, audio files, HTML projects, and render plans; rendering and dependency installation require user confirmation.]

## Skill Version(s):

1.1.3 (source: server release evidence; artifact frontmatter reports 1.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
