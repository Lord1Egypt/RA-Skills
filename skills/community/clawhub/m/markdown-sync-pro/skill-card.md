## Description: <br>
Markdown Sync Pro publishes Markdown content to Notion, GitHub Wiki, Medium, or local HTML. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonia-sz](https://clawhub.ai/user/antonia-sz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and content maintainers use this skill to preview, configure, and publish Markdown documents across supported documentation and publishing platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown documents or embedded images may contain secrets, private data, or content that should not be published. <br>
Mitigation: Use dry-run first and review documents and images before publishing. <br>
Risk: Platform tokens can grant access beyond what the publishing workflow needs. <br>
Mitigation: Use least-privilege GitHub, Notion, and Medium tokens and keep credentials in environment variables. <br>
Risk: The README includes a direct-use path involving an external repository or executable. <br>
Mitigation: Review the external repository and executable before running that path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/antonia-sz/markdown-sync-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands and platform configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish content to external platforms or export local HTML; supports dry-run preview.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.yaml, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
