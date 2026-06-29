## Description: <br>
Guides developers converting a client-side Next.js App Router static export into an Electron desktop app, including offline Windows packaging, custom app protocol setup, locale and window persistence, system tray behavior, and GitHub Actions builds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rockbenben](https://clawhub.ai/user/rockbenben) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to wrap static-export Next.js applications in Electron for Windows desktop distribution, especially for offline or intranet machines without WebView2. It provides implementation guidance, shell commands, configuration, and copy-paste templates for Electron, electron-builder, and CI release workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Electron and GitHub Actions templates may not match the target repository's project names, checkout branch, release permissions, or contents:write policy. <br>
Mitigation: Review and adjust generated templates before use, especially app identifiers, workflow refs, release upload behavior, and repository permissions. <br>
Risk: Desktop packaging guidance affects local application state and must be verified on the intended Windows runtime environment. <br>
Mitigation: Confirm local persistence is limited to expected app state such as locale and window size, then test the built app on target Windows machines before distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rockbenben/nextjs-to-electron) <br>
- [electron-files.md](electron-files.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and code/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project-specific instructions and copy-paste Electron, electron-builder, and GitHub Actions templates.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
