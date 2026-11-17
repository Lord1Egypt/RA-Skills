## Description:

Guides developers through converting a static-exportable Next.js app into a Windows Electron desktop app, especially for offline environments without WebView2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rockbenben](https://clawhub.ai/user/rockbenben)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to assess whether a Next.js app can be statically exported and to adapt it into a Windows Electron desktop app. It provides implementation templates and delivery guidance for offline environments, while identifying runtime server features and cross-platform packaging as out of scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example release workflow publishes tagged releases automatically, and one linked component was only partially inspected.

Mitigation: Before adopting the templates, review the release workflow and its repository changes, and independently inspect the linked component.

## Reference(s):

- [electron-files.md implementation templates](electron-files.md)
- [Skill homepage (ClawHub metadata)](https://github.com/rockbenben/aishort-skills/tree/main/skills/nextjs-to-electron)
- [Next.js static export documentation](https://nextjs.org/docs/app/guides/static-exports#supported-features)
- [Electron releases](https://releases.electronjs.org/releases.json)
- [Node.js release schedule](https://raw.githubusercontent.com/nodejs/Release/main/schedule.json)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JavaScript, YAML, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Implementation templates and adaptation notes; no fixed output size.]

## Skill Version(s):

1.1.17 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
