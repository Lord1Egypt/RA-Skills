## Description: <br>
Pexels helps agents search and retrieve Pexels photo, video, collection, and account collection metadata through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent find Pexels photos and videos, inspect item metadata, browse curated or popular media, and access Pexels collections through an authenticated OOMOL connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials through an authenticated OOMOL-connected Pexels account. <br>
Mitigation: Use the least-privileged connected account available, review requested commands before approval, and reconnect only when auth or scope errors require it. <br>
Risk: The skill can guide an agent to run powerful authenticated CLI commands. <br>
Mitigation: Review command payloads and expected effects before execution, especially if future connector actions are tagged as write or destructive. <br>
Risk: Billing or connection state can stop successful connector execution. <br>
Mitigation: Follow the documented setup fallback only after an action fails with an auth, connection, scope, or billing error. <br>


## Reference(s): <br>
- [ClawHub Pexels skill page](https://clawhub.ai/oomol/oo-pexels) <br>
- [Pexels homepage](https://www.pexels.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
