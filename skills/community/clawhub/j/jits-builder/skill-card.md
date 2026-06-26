## Description: <br>
Jits Builder helps an agent generate single-file vanilla JavaScript mini-apps from text or voice requests and expose them through Cloudflare tunnel URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dannyshmueli](https://clawhub.ai/user/dannyshmueli) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to create quick single-page utilities, serve them locally, and receive temporary public URLs for sharing or testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated local apps may become publicly reachable through Cloudflare tunnel URLs. <br>
Mitigation: Use only with intentionally public, non-sensitive mini-apps; avoid secrets, private business data, and unsafe generated code. <br>
Risk: The skill runs a Cloudflare tunnel binary from /tmp and evidence notes weak input controls. <br>
Mitigation: Prefer a hardened version that verifies cloudflared from an official source outside /tmp, validates app names and ports, asks before public deployment, and offers local-only mode. <br>
Risk: Running apps and tunnels can remain active until stopped. <br>
Mitigation: List and stop active apps after use, and prefer automatic cleanup for long-running environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dannyshmueli/jits-builder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated HTML, CSS, JavaScript, shell commands, and public URL text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated apps are single-file client-side HTML documents served locally and optionally exposed through temporary Cloudflare tunnel URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
