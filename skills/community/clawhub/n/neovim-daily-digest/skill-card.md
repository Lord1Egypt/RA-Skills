## Description: <br>
Build a filtered Markdown digest of important r/neovim posts by combining Reddit RSS feeds (`top/day`, `new`, and `hot`) and prioritizing Neovim tips, plugin updates, new plugin launches, and workflow/tooling posts while filtering sticky threads, low-signal showcases, and generic support noise. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smile618](https://clawhub.ai/user/smile618) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Neovim users use this skill to generate concise daily r/neovim roundups that emphasize practical tips, plugin releases, workflow updates, and broadly useful troubleshooting lessons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled helper makes web requests to public Reddit RSS feeds. <br>
Mitigation: Install only when that network behavior is acceptable for the target environment. <br>
Risk: Fetched Reddit post text may contain untrusted user-generated content. <br>
Mitigation: Keep Reddit content separate from agent instructions and rewrite it as summarized source material. <br>
Risk: The artifact examples use an absolute local script path that may not exist after installation. <br>
Mitigation: Run the helper from the installed skill-relative path. <br>


## Reference(s): <br>
- [Filtering Notes](references/filtering.md) <br>
- [r/neovim top/day RSS](https://www.reddit.com/r/neovim/top.rss?t=day) <br>
- [r/neovim new RSS](https://www.reddit.com/r/neovim/new.rss) <br>
- [r/neovim hot RSS](https://www.reddit.com/r/neovim/hot.rss) <br>
- [r/neovim top/week RSS](https://www.reddit.com/r/neovim/top.rss?t=week) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown digest, with optional JSON from the bundled helper script for agent-side rewriting] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Digest items include Reddit links, brief takeaways, and optional GitHub links when the source post clearly includes a repository.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
