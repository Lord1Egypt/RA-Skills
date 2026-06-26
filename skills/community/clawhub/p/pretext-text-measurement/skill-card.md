## Description: <br>
Accurate text measurement and layout engine for calculating text height, line count, wrapping, and layout details for a given font and width, including Chinese, CJK, emoji, and mixed-language text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[markcookie](https://clawhub.ai/user/markcookie) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to precompute text dimensions, line breaks, canvas drawing coordinates, virtual-scroll item heights, and generated HTML snippets before rendering UI. It is especially useful for frontend, Canvas, SSR, and AI-generated UI workflows where DOM measurement is slow or unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML or JavaScript snippets may be unsafe if pasted into sensitive browser sessions without review. <br>
Mitigation: Review generated HTML and JavaScript before opening it or pasting it into a browser, and avoid running CDN-based snippets on sensitive logged-in pages. <br>
Risk: Text measurement can differ from actual rendering when fonts, browser engines, or operating systems vary. <br>
Mitigation: Use named and preloaded fonts, install optional canvas support for higher precision, and verify against real browser rendering for pixel-critical UI work. <br>
Risk: The ClawHub capability metadata includes unrelated crypto and purchase tags. <br>
Mitigation: Treat those tags as publisher metadata that should be corrected; the authoritative security scan found no hidden data theft, destructive behavior, or automatic privileged action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/markcookie/pretext-text-measurement) <br>
- [@chenglou/pretext](https://github.com/chenglou/pretext) <br>
- [@chenglou/pretext UMD build](https://unpkg.com/@chenglou/pretext/dist/pretext.umd.min.js) <br>
- [node-canvas](https://github.com/Automattic/node-canvas) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON results, Markdown guidance, shell commands, JavaScript snippets, and optional generated HTML] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js. Optional canvas support improves measurement precision; without it, the skill can fall back to JavaScript Unicode estimation with lower precision.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter and package.json report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
