## Description:

Pretext helps agents measure and lay out text for frontend, canvas, virtual-scroll, chat, and AI-generated UI workflows, including height, line count, line details, rich inline text, DOM snippets, and particle-text demos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markcookie](https://clawhub.ai/user/markcookie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to estimate text dimensions, wrapping, and line layout before rendering UI. It is most relevant for virtual scrolling, chat interfaces, canvas drawing, generated UI validation, and browser or Node.js text-layout utilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that the skill can generate active browser HTML and JavaScript with unsafe interpolation.

Mitigation: Review generated snippets before use, sanitize any user-controlled text or styling, and avoid pasting generated snippets into authenticated or sensitive pages.

Risk: The browser workflow references an unpinned CDN dependency.

Mitigation: Pin the dependency version or vendor the browser bundle before relying on generated browser snippets.

Risk: The security verdict is suspicious because the skill goes beyond passive text measurement.

Mitigation: Install only when the broader frontend helper behavior is needed and review the skill before deployment.

Risk: The artifact warns that text measurements can differ across fonts, browsers, operating systems, and fallback modes.

Mitigation: Use installed named fonts, ensure fonts are loaded before measuring, prefer canvas-backed measurement for precision, and verify critical layouts in the target browser.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/markcookie/skills/pretext-text-measurement)
- [Artifact README](artifact/README.md)
- [Upstream @chenglou/pretext project](https://github.com/chenglou/pretext)
- [node-canvas project](https://github.com/Automattic/node-canvas)
- [Pretext UMD browser dependency](https://unpkg.com/@chenglou/pretext/dist/pretext.umd.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance, JSON measurement results, shell commands, and generated HTML or JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; canvas is optional for higher-precision measurement and the fallback mode uses JavaScript Unicode estimates.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and package.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
