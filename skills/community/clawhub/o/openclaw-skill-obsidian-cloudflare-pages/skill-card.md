## Description: <br>
Publish selected Obsidian markdown from a vault to a static site and deploy to Cloudflare Pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidyoh](https://clawhub.ai/user/davidyoh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content publishers use this skill to select Markdown or Obsidian vault content, build it with Quartz, and deploy it to Cloudflare Pages. It supports setup, dependency checks, sync, build, deploy, and dry-run workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Basic Auth can write the chosen password into a generated deployment middleware file. <br>
Mitigation: Prefer environment-backed Basic Auth credentials, keep the workspace private, and review generated middleware before deployment. <br>
Risk: Publishing broad source folders can expose unintended Markdown content. <br>
Mitigation: Keep includeFolders narrow, use excludeFolders for private areas, and enable the publish frontmatter gate when content needs explicit review. <br>
Risk: The fallback Quartz setup path can clear a non-empty workspace when explicitly allowed. <br>
Mitigation: Use a dedicated workspace, run with --dry-run first, and set ALLOW_DESTRUCTIVE=1 only when the configured workspace can be cleared. <br>
Risk: Cloudflare deployment requires API credentials that could grant publishing access. <br>
Mitigation: Use a scoped Cloudflare token and avoid sharing or committing local .env files. <br>


## Reference(s): <br>
- [Cloudflare Pages](https://pages.cloudflare.com/) <br>
- [Obsidian Web Clipper](https://obsidian.md/clipper) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate local configuration, sync selected Markdown files, build a static site, create optional Basic Auth middleware, and deploy through Wrangler.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
