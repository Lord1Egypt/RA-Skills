## Description: <br>
Guides developers through converting a static-export Next.js 16 App Router web app into a Tauri 2 desktop app with packaging, updater, i18n, and CI templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rockbenben](https://clawhub.ai/user/rockbenben) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to migrate compatible client-side Next.js applications into desktop builds, adding Tauri configuration, frontend integration hooks, signing reminders, and GitHub Actions release workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A leaked Tauri updater private key could let an attacker sign malicious updates that clients trust. <br>
Mitigation: Keep the private key out of source control, store it only as a GitHub secret for intended release repositories, and rotate it if exposure is suspected. <br>
Risk: The build workflow grants release permissions and can publish signed artifacts. <br>
Mitigation: Enable the workflow only in repositories where release publishing is intended and review copied permissions before use. <br>
Risk: The optional language persistence hook stores a preferred language locally, which has a small privacy tradeoff. <br>
Mitigation: Persist the preferred language only after the user explicitly chooses one, or omit the hook when cross-launch language memory is unnecessary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rockbenben/skills/nextjs-to-tauri) <br>
- [Frontend integration templates](artifact/frontend-integration.md) <br>
- [Tauri file templates](artifact/tauri-files.md) <br>
- [Desktop build workflow template](artifact/desktop-build.yml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code blocks and copy-paste configuration templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes project-specific placeholders and reminders to verify current dependency and action versions before applying.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
