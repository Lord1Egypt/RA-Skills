## Description:

PPT Generator converts user scripts into Jobs-style, minimalist, tech-themed vertical HTML presentations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunerw-dev](https://clawhub.ai/user/sunerw-dev)

### License/Terms of Use:


## Use Case:

Creators, employees, and developers use this skill to turn a talk script into a condensed Markdown script, slide outline, and ready-to-run 9:16 HTML presentation with keyboard and touch navigation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated presentations may contact third-party CDNs for scripts and fonts when opened.

Mitigation: For sensitive, offline, or restricted environments, replace CDN-hosted TailwindCSS and font resources with bundled or locally hosted resources before sharing the HTML.

## Reference(s):

- [Design Specification](artifact/references/design-spec.md)
- [Slide Types](artifact/references/slide-types.md)
- [ClawHub Skill Page](https://clawhub.ai/sunerw-dev/skills/ppt-generator-1)
- [TailwindCSS CDN Used by Generated HTML](https://lf26-cdn-tos.bytecdntp.com/cdn/expire-1-M/tailwindcss/3.0.23/tailwind.min.js)
- [Font CSS Used by Generated HTML](https://fonts.loli.net/css2?family=Noto+Sans+SC:wght@300;400;700;900&display=swap)
- [Inter Font CSS Used by Generated HTML](https://fonts.loli.net/css2?family=Inter:wght@300;400;700;900&display=swap)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code]

**Output Format:** [Markdown response containing a refined script, slide outline, and complete single-file HTML code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML targets a 9:16 vertical presentation and may load TailwindCSS and font resources from third-party CDNs when opened.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
