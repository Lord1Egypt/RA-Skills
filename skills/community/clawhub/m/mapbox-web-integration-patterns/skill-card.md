## Description: <br>
Official integration patterns for Mapbox GL JS across popular web frameworks, covering setup, lifecycle management, token handling, search integration, and common pitfalls based on Mapbox's create-web-app scaffolding tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mapbox](https://clawhub.ai/user/mapbox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to implement, review, and debug Mapbox GL JS integrations across React, Vue, Svelte, Angular, Next.js, vanilla JavaScript, and Web Components. It focuses on lifecycle cleanup, token handling, Search JS integration, framework-specific setup, and common pitfalls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mapbox public tokens can be exposed or over-permissive if copied directly into source code or left unrestricted. <br>
Mitigation: Use environment variables, keep tokens out of source control, and restrict public token scopes and allowed origins before production use. <br>
Risk: Map search and geolocation examples may send user-entered locations or map interaction data to Mapbox services. <br>
Mitigation: Disclose Mapbox data flows to users and confirm privacy, retention, and consent requirements before enabling search or location features. <br>
Risk: Framework and package examples may drift as Mapbox GL JS, Search JS, and web frameworks release new versions. <br>
Mitigation: Verify package names, versions, and framework integration requirements against current Mapbox documentation before copying examples into production. <br>
Risk: Incorrect map lifecycle handling can create memory leaks, repeated WebGL contexts, or broken server-side rendering. <br>
Mitigation: Initialize maps in the appropriate client-side lifecycle hook, wait for map load before adding sources or layers, and call map.remove() during cleanup. <br>


## Reference(s): <br>
- [Mapbox GL JS Documentation](https://docs.mapbox.com/mapbox-gl-js/) <br>
- [Mapbox Search JS Documentation](https://docs.mapbox.com/mapbox-search-js/) <br>
- [create-web-app GitHub](https://github.com/mapbox/create-web-app) <br>
- [Angular Integration](references/angular.md) <br>
- [Common Mistakes and Testing Patterns](references/common-mistakes.md) <br>
- [Next.js Integration](references/nextjs.md) <br>
- [Svelte Integration](references/svelte.md) <br>
- [Token Management Patterns](references/token-management.md) <br>
- [Vanilla JavaScript Integration](references/vanilla.md) <br>
- [Vue Integration](references/vue.md) <br>
- [Web Components](references/web-components.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; examples require project-specific validation before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
