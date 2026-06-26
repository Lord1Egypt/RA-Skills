## Description: <br>
Helps build a single-file Markdown-to-HTML converter with multiple blog themes, real-time preview, file upload, syntax highlighting, and HTML download support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wings229](https://clawhub.ai/user/wings229) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to build a browser-based converter for turning Markdown documents into styled HTML previews and downloadable pages. It is useful when an agent needs implementation guidance for themes, layout, upload handling, parsing, preview updates, and exported HTML. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated previews or downloadable HTML may be unsafe when processing sensitive or untrusted Markdown without sanitization. <br>
Mitigation: Sanitize rendered HTML and avoid placing unsanitized user Markdown into trusted pages or privileged contexts. <br>
Risk: The artifact describes CDN dependencies while also presenting offline use as a goal. <br>
Mitigation: Bundle or pin dependencies with integrity checks, and document that offline use requires local copies of the parser and highlighter assets. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wings229/markdown2html-converter) <br>
- [Marked CDN dependency](https://cdn.jsdelivr.net/npm/marked/marked.min.js) <br>
- [highlight.js stylesheet dependency](https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/github.min.css) <br>
- [highlight.js script dependency](https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with HTML, CSS, and JavaScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single-file web app guidance; generated HTML may rely on CDN-hosted marked.js and highlight.js unless dependencies are bundled or pinned.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
