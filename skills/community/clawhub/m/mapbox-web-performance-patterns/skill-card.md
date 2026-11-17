## Description:

Provides prioritized performance optimization patterns for Mapbox GL JS web applications, covering initialization waterfalls, bundle size, rendering performance, memory management, and web optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapbox](https://clawhub.ai/user/mapbox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review and improve Mapbox GL JS web apps, especially initial loading, large data rendering, interaction responsiveness, mobile behavior, and SPA memory management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Popup examples use setHTML() with map feature properties, which can lead to XSS-prone code when data is untrusted.

Mitigation: Use setText() for plain text popup content, or sanitize HTML with a maintained sanitizer before rendering API, GeoJSON, vector-tile, uploaded, or third-party data.

Risk: The skill is performance guidance, not secure coding guidance.

Mitigation: Review generated code before adoption and apply the security guidance from the release evidence when adapting examples.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/mapbox/skills/mapbox-web-performance-patterns)
- [Data Loading Optimization](references/data-loading.md)
- [Optimize Map Interactions](references/interactions.md)
- [Layer and Style Performance](references/layers-styles.md)
- [Memory Management](references/memory.md)
- [Mobile Performance](references/mobile.md)
- [Mapbox Tiling Service guides](https://docs.mapbox.com/mapbox-tiling-service/guides/)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with JavaScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review popup rendering suggestions for untrusted data before use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
