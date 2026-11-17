## Description:

Create professional posters and visual designs using Gemini image generation for event posters, product showcases, announcements, and social media graphics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andylikescodes](https://clawhub.ai/user/andylikescodes)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate poster concepts, production-ready poster images, and optional text overlays for events, products, announcements, promotions, and social media posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The composition helper can execute shell commands built from poster text or paths when ImageMagick is available.

Mitigation: Do not run the composition helper on untrusted text or file paths until command execution is replaced with argument-based process execution and inputs are sanitized.

Risk: Gemini image generation requires an API key that could be exposed if stored or logged carelessly.

Mitigation: Use a protected GEMINI_API_KEY from environment variables or secure secret storage and do not commit .env files.

Risk: The HTML composition fallback can include user-provided poster text.

Mitigation: Sanitize or escape fallback HTML content before using it with untrusted poster text.

## Reference(s):

- [Gemini Image Generation API Reference](references/api-docs.md)
- [Poster Templates Reference](references/templates.md)
- [Job Queue System for Image Generation](references/queue-system.md)
- [Rate Limiting Configuration](references/rate-limiting.md)
- [Gemini API Key Setup](https://makersuite.google.com/app/apikey)
- [Gemini generateContent API Endpoint](https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; bundled scripts can produce PNG image files, HTML composition files, and JSON metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a protected GEMINI_API_KEY for image generation; optional composition depends on ImageMagick or falls back to HTML output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
