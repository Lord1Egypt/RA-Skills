## Description:

Build halftone dot art for web: CSS, canvas, SVG, React.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sakib-dalal](https://clawhub.ai/user/sakib-dalal)

### License/Terms of Use:

MIT-0

## Use Case:

Web developers use this skill to create print-inspired halftone visuals for pages, posters, and other web graphics. It guides technique selection and provides CSS, canvas, SVG, and React implementations, including transparent cutouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local HTML previews need a web server for canvas pixel access, and an exposed preview could make files available beyond the local machine.

Mitigation: Preview only a dedicated asset folder with python3 -m http.server 8000 --bind 127.0.0.1 --directory <preview-folder>, then stop the server afterward.

Risk: Bundled pages request fonts from Google, which makes those font requests external network activity.

Mitigation: Use system or self-hosted fonts to avoid Google requests.

## Reference(s):

- [Design language](artifact/references/design-language.md)
- [Techniques](artifact/references/techniques.md)
- [ClawHub release](https://clawhub.ai/sakib-dalal/skills/halftone-art)
- [Publisher profile](https://clawhub.ai/user/sakib-dalal)

## Skill Output:

**Output Type(s):** [Code, Files, Guidance]

**Output Format:** [HTML, CSS, JavaScript, SVG, and TypeScript/React code with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runnable web templates, a zero-dependency canvas engine, React bindings, and responsive design guidance.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
