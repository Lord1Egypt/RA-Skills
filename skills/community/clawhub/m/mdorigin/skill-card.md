## Description: <br>
Build, preview, and deploy markdown-first sites with local preview, Cloudflare bundles, and agent-readable raw markdown routes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to install and run mdorigin commands for markdown-first publishing sites, including local preview, index and search generation, Cloudflare bundle output, R2 sync, and markdown-aware routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install and run the mdorigin npm package. <br>
Mitigation: Verify that the npm package is the intended mdorigin package, and prefer a project-local or pinned install when practical. <br>
Risk: Cloudflare and R2 sync or init commands can affect the wrong directory, bucket, or account when run with active credentials. <br>
Mitigation: Confirm the target directory, bucket name, and active credentials before running Cloudflare/R2 commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jolestar/mdorigin) <br>
- [mdorigin HTML docs](https://mdorigin.jolestar.workers.dev) <br>
- [mdorigin raw markdown home](https://mdorigin.jolestar.workers.dev/README.md) <br>
- [Routing docs](https://mdorigin.jolestar.workers.dev/concepts/routing.md) <br>
- [Configuration docs](https://mdorigin.jolestar.workers.dev/reference/configuration.md) <br>
- [Extensions docs](https://mdorigin.jolestar.workers.dev/guides/extensions.md) <br>
- [Cloudflare docs](https://mdorigin.jolestar.workers.dev/guides/cloudflare.md) <br>
- [OpenAPI schema](https://mdorigin.jolestar.workers.dev/api/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include npm install commands, mdorigin CLI commands, Cloudflare/R2 deployment steps, and links to mdorigin documentation.] <br>

## Skill Version(s): <br>
0.2.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
