## Description:

Convert Markdown heading outlines into themed KMind mind maps. Export PNG or SVG images with theme presets, layouts, edge routes, dark mode, and rainbow branches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suka233](https://clawhub.ai/user/suka233)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and teams use this skill to turn Markdown heading outlines for meetings, notes, brainstorming, and proposals into polished KMind mind map images or editable KMind project files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic PNG or SVG export launches a local Chromium browser session to render Markdown.

Mitigation: Use the skill only where local browser rendering is acceptable, and use manual browser mode or .kmindz.svg export when automatic Chromium launch is unavailable.

Risk: Rendered Markdown is visible to the temporary local browser session.

Mitigation: Avoid rendering sensitive content on shared or untrusted machines, and close the browser session after export.

Risk: Untrusted local processes could attempt to race localhost render endpoints during browser-based export.

Mitigation: Run exports on a trusted local machine and avoid concurrent untrusted local processes during rendering.

Risk: Incorrect output paths could overwrite or place generated files somewhere unintended.

Mitigation: Choose explicit output paths and review them before running the generated Node command.

## Reference(s):

- [KMind Zen](https://kmind.app)
- [ClawHub skill page](https://clawhub.ai/suka233/skills/kmind-markdown-to-mindmap)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Node.js shell commands that produce PNG, SVG, or .kmindz.svg files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PNG is the recommended default image output; automatic PNG and SVG export require local Chromium, while .kmindz.svg export does not depend on browser rendering.]

## Skill Version(s):

0.1.1 (source: frontmatter, package.json, CHANGELOG released 2026-05-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
