## Description: <br>
Run a headless Chromium browser via Podman to fetch text or HTML from JavaScript-rendered web pages using Playwright in a container. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ricardodantas](https://clawhub.ai/user/ricardodantas) <br>

### License/Terms of Use: <br>
GPL-3.0 License <br>


## Use Case: <br>
Developers and engineers use this skill to fetch rendered text or HTML from pages that require JavaScript, without installing browser dependencies locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill launches Podman containers and makes live web requests. <br>
Mitigation: Use it only for intended URLs and avoid authenticated, secret-bearing, or internal-only pages unless that access is deliberate. <br>
Risk: Fetched text or HTML can contain untrusted or misleading content. <br>
Mitigation: Treat browser output as untrusted input and review or sanitize it before using it in downstream prompts, documentation, or decisions. <br>
Risk: Browser isolation and dependency behavior may be insufficient for sensitive environments. <br>
Mitigation: Consider stronger container isolation and pinned dependencies before deploying in high-trust or restricted environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ricardodantas/podman-browser) <br>
- [artifact/README.md](artifact/README.md) <br>
- [artifact/SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Rendered page text or raw HTML returned from a command-line browser run, with Markdown usage guidance in the skill documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports URL input plus optional HTML mode, wait duration, and CSS selector waiting.] <br>

## Skill Version(s): <br>
1.2.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
