## Description: <br>
Publish selected Obsidian markdown from a vault to a static site and deploy to Cloudflare Pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidyoh](https://clawhub.ai/user/davidyoh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical users use this skill to publish selected Obsidian or Markdown notes as a Quartz static site and deploy it to Cloudflare Pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The publishing CLI can delete files in configurable local paths. <br>
Mitigation: Use a dedicated empty workspace and verify workspaceDir, contentDir, include folders, exclude folders, and generated content before running the full pipeline. <br>
Risk: Setup and deployment may run unpinned external commands. <br>
Mitigation: Review the CLI behavior before execution and start with a test Cloudflare Pages project. <br>
Risk: Cloudflare API credentials are required for deployment. <br>
Mitigation: Use least-privileged Cloudflare tokens, keep secrets out of chat, and store them only in the intended environment or local .env file. <br>
Risk: Optional Basic Auth is not sufficient protection for highly sensitive notes. <br>
Mitigation: Avoid publishing highly sensitive content unless a stronger security model and deployment hardening are in place. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/davidyoh/obsidian-cloudflare-pages-skill) <br>
- [Cloudflare Pages](https://pages.cloudflare.com/) <br>
- [Obsidian Web Clipper](https://obsidian.md/clipper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, and generated static-site deployment files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local configuration, synchronized Markdown content, Quartz build output, optional Basic Auth middleware, and Cloudflare Pages deployment commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
