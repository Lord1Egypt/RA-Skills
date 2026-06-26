## Description: <br>
Multi-column chat deck UI for OpenClaw agents. Launch a local web interface to manage and chat with multiple agents side-by-side. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kellyclaudeai](https://clawhub.ai/user/kellyclaudeai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and launch a local Vite web interface for managing multiple OpenClaw chat columns side-by-side. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gateway tokens may be exposed through browser-visible URL parameters or VITE_ environment variables. <br>
Mitigation: Use short-lived, least-privilege gateway tokens and avoid placing long-lived or broadly privileged tokens in URLs or browser-exposed configuration. <br>
Risk: The page loads Google Fonts from an external service. <br>
Mitigation: Review network access expectations before use, or self-host fonts in environments that restrict third-party requests. <br>
Risk: The multi-column UI may not map each column to a separate backend agent. <br>
Mitigation: Verify OpenClaw Gateway routing behavior before relying on columns as isolated agent sessions. <br>


## Reference(s): <br>
- [OpenClaw Gateway Architecture](https://docs.openclaw.ai/concepts/architecture) <br>
- [ClawHub Skill Page](https://clawhub.ai/kellyclaudeai/openclaw-deck) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with local commands and URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Launches a local Vite UI that connects to an OpenClaw Gateway.] <br>

## Skill Version(s): <br>
0.1.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
