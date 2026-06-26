## Description: <br>
Cloudflare Worker (workers.cloudflare.com). Use this skill for any Cloudflare Worker request, including reading, creating, updating, and deleting Cloudflare Worker resources through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Cloudflare Workers, scripts, settings, and secrets through the OOMOL oo CLI after inspecting the live connector schema for each action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloudflare Worker source, settings, account data, and secret-related reads may expose sensitive information. <br>
Mitigation: Check Cloudflare account scopes before use and treat source and secret-related reads as sensitive. <br>
Risk: Write, upload, secret change, and delete actions can alter or remove live Cloudflare Worker resources. <br>
Mitigation: Require exact target and payload confirmation before uploads, writes, secret changes, or deletes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/skills/oo-cloudflare-worker) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [Cloudflare Workers](https://workers.cloudflare.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads; connector responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live action schema inspection before execution; write, upload, secret, and destructive actions require exact user confirmation.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
