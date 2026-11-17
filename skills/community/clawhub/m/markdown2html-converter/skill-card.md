## Description:

Use when building a Markdown to HTML converter with multiple blog themes, real-time preview, and download functionality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wings229](https://clawhub.ai/user/wings229)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content authors use this skill to build a single-file web app that converts Markdown into styled HTML with live preview, theme selection, file upload, sample loading, and HTML download support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser dependencies are loaded from CDNs without vendoring, version pinning, or integrity hashes.

Mitigation: Vendor or pin dependencies and add integrity hashes before release or before use in sensitive environments.

Risk: The skill describes offline use while its generated app guidance depends on external CDN resources.

Mitigation: Remove or clarify the offline-use claim unless all required assets are bundled locally.

Risk: Markdown preview and downloaded HTML can expose users to unsafe HTML when processing untrusted Markdown.

Mitigation: Add HTML sanitization and a restrictive preview/download security boundary before accepting untrusted Markdown.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wings229/skills/markdown2html-converter)
- [marked.js CDN dependency](https://cdn.jsdelivr.net/npm/marked/marked.min.js)
- [highlight.js GitHub theme CDN dependency](https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/github.min.css)
- [highlight.js script CDN dependency](https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js)

## Skill Output:

**Output Type(s):** [Markdown, Code, Files, Guidance]

**Output Format:** [Markdown guidance with HTML, CSS, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically describes a single-file index.html app with CDN dependencies and browser-based preview/download behavior.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
