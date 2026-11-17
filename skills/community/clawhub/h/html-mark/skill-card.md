## Description:

Adds a self-contained click-to-annotate overlay to HTML pages so reviewers can place pinned notes and export feedback as Markdown, plain text, JSON, or an AI handoff with selectors and HTML snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuxinmaxen](https://clawhub.ai/user/xuxinmaxen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and product reviewers use this skill to add annotation overlays to HTML prototypes or pages they are authorized to review, then collect pinned feedback for review tools or coding agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runtime can be injected into arbitrary live sites and may capture page content in notes, selectors, or HTML snapshots.

Mitigation: Use it mainly on local prototypes or pages you own or are authorized to review; avoid authenticated, production, financial, healthcare, admin, or third-party pages.

Risk: Clipboard exports can include captured page content and reviewer notes.

Mitigation: Review and redact Markdown, JSON, and For AI exports before pasting them into AI tools or shared systems.

Risk: Hosted bookmarklet variants depend on externally loaded script URLs and may be blocked by strict Content Security Policy.

Mitigation: Prefer local or self-contained injection for prototypes; use hosted assets only when the hosting location and page policy are acceptable.

## Reference(s):

- [Html Mark on ClawHub](https://clawhub.ai/xuxinmaxen/skills/html-mark)
- [HTML Mark README](README.md)
- [Basic injection example](examples/basic.md)
- [Advanced bookmarklet example](examples/advanced.md)
- [Live demo](https://xuxinmaxen.github.io/html-mark/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell, HTML, JavaScript, JSON, and plain text export examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a self-contained html-mark runtime injection workflow or bookmarklet guidance; annotation exports may include page selectors and HTML snapshots.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
