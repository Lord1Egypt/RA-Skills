## Description:

Publish selected Obsidian markdown from a vault to a static site and deploy to Cloudflare Pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidyoh](https://clawhub.ai/user/davidyoh)

### License/Terms of Use:


## Use Case:

Developers, engineers, and Obsidian users use this skill to publish selected Markdown notes as a static site on Cloudflare Pages. It helps configure a publishing workspace, sync allowed content, build with Quartz, and deploy with Wrangler.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell command construction and configurable destructive deletion can affect files reachable through configured publish paths.

Mitigation: Run the skill only in a dedicated workspace with backed-up content and no valuable files under configured publish or workspace directories.

Risk: Cloudflare credentials and optional Basic Auth settings can expose sensitive deployment access or plaintext passwords.

Mitigation: Use a narrowly scoped Cloudflare Pages token, keep secrets out of chat and committed files, and avoid Basic Auth until password handling uses Cloudflare secrets or another managed secret store.

Risk: Unpinned Quartz and Wrangler tooling can change behavior between runs.

Mitigation: Review and pin the Quartz and Wrangler versions before production deployment.

## Reference(s):

- [Cloudflare Pages](https://pages.cloudflare.com/)
- [Obsidian Web Clipper](https://obsidian.md/clipper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to create or update local configuration files and run publish, build, and deploy commands.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
