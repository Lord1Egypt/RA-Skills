# Security and privacy notes

This skill is designed for paper reading, report generation, staged visual planning, and local image-PDF assembly.

## Data handling

- The skill should use only user-provided papers, uploaded artifacts, and explicitly approved sources.
- The deep-reading phase must not browse external sources unless the user explicitly requests a retrieval stage or the surrounding platform requires verification.
- The image-generation phase should use only the content already summarized in the report and the user-approved visual plan.
- The final PDF assembly step should combine already-generated images locally and should not call external services.

## API usage

- ChatGPT web/app: use Create image when the user starts an image step.
- Codex / Claude Code / coding-agent environments: prefer the `imagegen` skill when available. If it is unavailable or insufficient, use ChatGPT Images 2.0 API or another user-approved image-generation API.
- Do not embed API keys or credentials in outputs.

## Runtime declarations

This package includes optional Python helper scripts. It declares Python as an optional/alternative binary requirement through `metadata.openclaw.requires.anyBins`.

## License

Published ClawHub skills are released under MIT-0; this package declares MIT-0 in metadata and documentation and does not add conflicting terms.
