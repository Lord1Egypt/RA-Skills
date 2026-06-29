## Description: <br>
YanDu DECK turns articles or topics into one-screen-per-idea, paginated and auto-playing keynote-style web decks with dark or light themes, self-hosted fonts, and Cloudflare Pages publishing support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huiyonghkw](https://clawhub.ai/user/huiyonghkw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content publishers use this skill to convert article content into immersive web presentation decks, manage deck and homepage assets, self-host fonts, and build or publish the site to Cloudflare Pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish changes to a live Cloudflare Pages site. <br>
Mitigation: Verify the destination account and site, run build-only or preview commands first, and require explicit confirmation before production publishing. <br>
Risk: The skill can edit deck project files and change local publishing assets. <br>
Mitigation: Review file changes before deployment, keep the working scope limited to the intended deck project, and scan the skill before use. <br>
Risk: Publishing depends on a locally installed and authenticated Wrangler setup. <br>
Mitigation: Install Wrangler independently, confirm the active Cloudflare account, and avoid reusing stale credentials for unintended sites. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/huiyonghkw/hekouwang-yandu-deck-skill) <br>
- [YanDu DECK live site](https://hekouwang.pages.dev) <br>
- [System notes](references/系统说明.md) <br>
- [Demo HTML](examples/demo.html) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with HTML, CSS, Python, shell commands, and configuration edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify deck HTML, homepage templates, font packaging outputs, and Cloudflare Pages build or deploy commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
