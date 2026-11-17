## Description:

Provides Go structured logging guidance for samber/slog packages, covering multi-handler pipelines, sampling, attribute formatting, HTTP middleware, and backend routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Go slog pipelines with samber/slog handlers for sampling, PII-aware formatting, HTTP request logging, level-based routing, and backend sinks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTTP logging examples may lead agents to include sensitive request or response data in shared or third-party logging systems.

Mitigation: Keep request and response body logging disabled by default, avoid Authorization and Cookie headers or client identifiers unless explicitly approved, and apply redaction before remote sinks.

Risk: Remote backend and batch-handler examples can lose buffered logs or expose data beyond the process boundary if configured casually.

Mitigation: Use approved sinks with appropriate retention, flush or close batch handlers during graceful shutdown, and restrict raw payload logging to approved non-sensitive endpoints.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/samber/skills/golang-samber-slog)
- [samber cc-skills-golang](https://github.com/samber/cc-skills-golang)
- [samber/slog-multi](https://github.com/samber/slog-multi)
- [samber/slog-sampling](https://github.com/samber/slog-sampling)
- [samber/slog-formatter](https://github.com/samber/slog-formatter)
- [Pipeline Patterns](references/pipeline-patterns.md)
- [Sampling Strategies](references/sampling-strategies.md)
- [HTTP Middlewares](references/http-middlewares.md)
- [Backend Handlers](references/backend-handlers.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Go code examples and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend Go package imports, handler composition patterns, middleware settings, and operational checks for logging pipelines.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
