## Description: <br>
Publishes a single self-contained HTML page to htmlcode.fun and manages stable short codes, versioned updates, source reads, unlocked-version edits, and preservation hints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[520xiaomumu](https://clawhub.ai/user/520xiaomumu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to publish or update single-file HTML pages on htmlcode.fun when they need fast shareable links for demos, landing pages, reports, QR pages, or AI-generated frontends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HTML deployed through this skill becomes available through a public htmlcode.fun link. <br>
Mitigation: Review each page before deployment for secrets, private data, tracking code, and embedded assets that should not be public. <br>
Risk: Overwrite, unpublish, switch-current, and delete actions can change what visitors see. <br>
Mitigation: Inspect version history first, avoid changing liked versions, append a new version when preservation matters, and ask before destructive actions unless the user explicitly requested them. <br>
Risk: The skill is a fast single-file publication path, not a full production hosting platform. <br>
Mitigation: Use a dedicated host such as Vercel, Netlify, GitHub Pages, or an application platform when a site needs multi-file assets, build steps, server logic, secrets, custom domains, or production workflows. <br>


## Reference(s): <br>
- [htmlcode.fun live guide](https://www.htmlcode.fun/s/htmlcode-fun-guide) <br>
- [htmlcode.fun](https://www.htmlcode.fun) <br>
- [ClawHub skill page](https://clawhub.ai/520xiaomumu/html-deploy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns deployment URLs, version metadata, QR code data, retry guidance, and preserve hints when provided by htmlcode.fun.] <br>

## Skill Version(s): <br>
1.3.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
