## Description: <br>
Autonomous browser automation for AI agents using agent-browser for step-by-step Playwright control and browser-use for autonomous web tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinj0012](https://clawhub.ai/user/yinj0012) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to automate dynamic web interactions, including navigation, form filling, scraping, authenticated session workflows, screenshots, and autonomous multi-step browsing tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The autonomous browser can take broad web actions and interact with authenticated sessions. <br>
Mitigation: Run it only in trusted or disposable environments and avoid real logged-in accounts unless the workflow requires them. <br>
Risk: The wrapper can read API keys from /root/.openclaw/openclaw.json when environment variables are not set. <br>
Mitigation: Set scoped API keys explicitly and review or remove the local credential fallback before use. <br>
Risk: Saved auth state, cookies, screenshots, PDFs, recordings, and extracted page content can contain secrets. <br>
Mitigation: Treat generated browser artifacts as sensitive, restrict access to them, and delete them when no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yinj0012/openclaw-skill-browser-use) <br>
- [Browser workflow reference](references/browser-workflow.md) <br>
- [agent-browser npm package](https://www.npmjs.com/package/agent-browser) <br>
- [browser-use Python library](https://github.com/browser-use/browser-use) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown or shell output, with optional JSON and saved browser artifacts such as screenshots, PDFs, recordings, cookies, and storage state.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include browser session state and extracted page content; treat auth state, cookies, screenshots, PDFs, and recordings as sensitive.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
