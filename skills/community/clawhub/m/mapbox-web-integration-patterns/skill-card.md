## Description:

Official integration patterns for Mapbox GL JS across popular web frameworks (React, Vue, Svelte, Angular). Covers setup, lifecycle management, token handling, search integration, and common pitfalls. Based on Mapbox's create-web-app scaffolding tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapbox](https://clawhub.ai/user/mapbox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up, review, and troubleshoot Mapbox GL JS integrations across React, Vue, Svelte, Angular, Next.js, vanilla JavaScript, and Web Components. It provides framework-specific guidance for lifecycle management, cleanup, token handling, search integration, and common implementation mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mapbox browser tokens can be exposed or over-permissive in client-side applications.

Mitigation: Use public browser tokens, keep tokens in environment variables, restrict them in Mapbox settings, and avoid committing real .env files.

Risk: Unpinned package or CDN versions can change integration behavior over time.

Mitigation: Pin library versions for production builds and prefer npm-managed Mapbox GL JS versions over CDN snippets.

Risk: Browser geolocation can create privacy and consent concerns.

Mitigation: Add clear user-facing consent, fallback behavior, and error handling before using geolocation.

Risk: Incorrect lifecycle handling can leak WebGL contexts, DOM nodes, or event listeners.

Mitigation: Initialize the map once in the framework lifecycle and call map.remove() during component cleanup.

## Reference(s):

- [Mapbox GL JS Documentation](https://docs.mapbox.com/mapbox-gl-js/)
- [Mapbox Search JS Documentation](https://docs.mapbox.com/mapbox-search-js/)
- [create-web-app GitHub](https://github.com/mapbox/create-web-app)
- [Angular Integration](references/angular.md)
- [Common Mistakes and Testing Patterns](references/common-mistakes.md)
- [Next.js Specific Patterns](references/nextjs.md)
- [Svelte Integration](references/svelte.md)
- [Token Management Patterns](references/token-management.md)
- [Vanilla JavaScript Integration](references/vanilla.md)
- [Vue Integration](references/vue.md)
- [Web Components](references/web-components.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; does not execute tools or call external services by itself.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
