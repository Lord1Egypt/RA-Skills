## Description: <br>
Pincer is a security-first wrapper for installing agent skills that scans for malware, prompt injection, and suspicious patterns before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panzacoder](https://clawhub.ai/user/panzacoder) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use Pincer to scan ClawHub skills before installing them, audit installed skills, and manage trusted or blocked publishers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review found that install workflows may run installation actions before scanning in fallback cases and may auto-install clean results more broadly than documented. <br>
Mitigation: Set autoApprove to never, review ~/.config/pincer/config.json before use, and do not rely on Pincer as a strict pre-install barrier until the fallback install behavior is removed or explicitly confirmed. <br>
Risk: Pincer runs an unpinned external scanner, so scanner behavior can change between executions. <br>
Mitigation: Use it only where external scanner updates are acceptable, review scan output before installation, and pin or separately vet scanner dependencies for controlled environments. <br>


## Reference(s): <br>
- [Pincer on ClawHub](https://clawhub.ai/panzacoder/pincer) <br>
- [mcp-scan](https://github.com/invariantlabs-ai/mcp-scan) <br>
- [1Password Security Research: OpenClaw Agent Skills attack surface](https://1password.com/blog/from-magic-to-malware-how-openclaws-agent-skills-become-an-attack-surface) <br>
- [Snyk ToxicSkills Report](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Analysis, Configuration] <br>
**Output Format:** [Terminal text with optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local configuration and installation history files when its commands are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
