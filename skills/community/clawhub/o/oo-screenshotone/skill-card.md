## Description: <br>
ScreenshotOne helps an agent use an OOMOL-connected ScreenshotOne account to capture screenshots, animated captures, bulk captures, usage details, and device presets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill when they want an agent to capture website, HTML, or Markdown screenshots through their connected ScreenshotOne account. It also supports usage checks, device preset discovery, animated captures, and bulk screenshot submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshot inputs are shared with the connected OOMOL and ScreenshotOne services. <br>
Mitigation: Install and use the skill only when that data sharing is acceptable for the target URLs, HTML, or Markdown content. <br>
Risk: Bulk capture requests can send many screenshot jobs through the connected account. <br>
Mitigation: Review bulk capture payloads before execution and confirm the requested targets and volume are intentional. <br>
Risk: The optional CLI installer uses shell or PowerShell commands fetched from OOMOL-hosted URLs. <br>
Mitigation: Use automatic installation only when the OOMOL CLI source is trusted, or install the CLI through a reviewed internal process. <br>


## Reference(s): <br>
- [ScreenshotOne ClawHub skill page](https://clawhub.ai/oomol/oo-screenshotone) <br>
- [ScreenshotOne homepage](https://screenshotone.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON payloads; connector actions may return JSON metadata and screenshot, video, or GIF files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The agent should inspect the live action schema before building payloads and should review bulk capture requests before running them.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
