## Description: <br>
Huo15 Markdown Export helps agents convert existing Markdown documents into styled PDF, DOCX, HTML, long-image, WeChat inline HTML, preview, sharing, and publishing outputs using bundled themes and scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and agents use this skill to render existing Markdown into polished documents and publishing assets across PDF, Word, HTML, image, WeChat, preview, and share-ready workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install itself across multiple OpenClaw workspaces. <br>
Mitigation: Run install-to-workspaces.sh with --dry-run first and review affected paths before allowing workspace changes. <br>
Risk: Markdown rendering and publishing can persist or expose document contents. <br>
Mitigation: Avoid using the skill for sensitive documents unless archiving and sharing behavior is reviewed; use --no-archive where appropriate. <br>
Risk: Generated public links or chat-channel sends can disclose files to unintended recipients. <br>
Mitigation: Require explicit user confirmation before creating public links or sending generated files to external chat channels. <br>
Risk: Rendering untrusted Markdown may involve raw HTML or network-dependent content. <br>
Mitigation: Render only trusted Markdown unless raw HTML handling and network access are acceptable for the environment. <br>
Risk: Share or preview URLs may point to localhost, LAN, or link-local hosts that external recipients cannot access. <br>
Mitigation: Apply the unsafe host checks described in the release evidence and downgrade to file delivery or local paths when a URL uses an unsafe host. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-markdown-export) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>
- [Theme design guide](themes/DESIGN.md) <br>
- [Template documentation](templates/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated document files, plus JSON handoff data for share and publish workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce PDF, DOCX, HTML, PNG long images, WeChat inline HTML, local preview output, changelog PDFs, and share-ready file metadata.] <br>

## Skill Version(s): <br>
0.4.4 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
