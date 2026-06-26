## Description: <br>
Convert Markdown heading outlines into themed KMind mind maps with PNG, SVG, and editable KMind package export options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suka233](https://clawhub.ai/user/suka233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and teams use this skill to turn Markdown heading outlines for meetings, notes, brainstorming, and proposals into polished KMind mind map images or editable KMind project files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Node code and writes the requested output file. <br>
Mitigation: Install only from the trusted release, review requested output paths, and keep file writes limited to user-approved locations. <br>
Risk: PNG and SVG image export can launch Chromium and use a temporary localhost render session. <br>
Mitigation: Use automatic browser export only when local browser automation is acceptable; use manual mode or editable .kmindz.svg export when automation is unavailable. <br>
Risk: Release metadata includes crypto and purchasing capability tags that are not supported by the artifacts. <br>
Mitigation: Treat the skill only as a mind-map renderer and do not grant financial, crypto, or purchasing authority based on those tags. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suka233/kmind-markdown-to-mindmap) <br>
- [KMind Zen](https://kmind.app) <br>
- [README](artifact/README.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, guidance] <br>
**Output Format:** [PNG, SVG, editable .kmindz.svg, and concise command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local conversion requires Node.js; automatic PNG or SVG export requires a usable local Chromium browser.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter, package.json, CHANGELOG released 2026-05-18, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
