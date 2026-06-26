## Description: <br>
Provides multi-step browser automation patterns with tab management, login checks, stale reference recovery, and session handling for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronmda](https://clawhub.ai/user/aaronmda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to guide browser automation beyond a single page check, including tab reuse, login-state checks, action targeting, stale reference recovery, and manual blocker reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent operating in an existing logged-in browser session could perform sensitive actions such as purchases, account changes, form submissions, admin work, or public posting. <br>
Mitigation: Supervise sensitive browser actions and require user confirmation or manual completion for purchases, account changes, form submissions, admin work, public posting, login, CAPTCHA, 2FA, and permission prompts. <br>
Risk: Stale browser references or duplicated tabs can lead the agent to act on the wrong page or control. <br>
Mitigation: Use stable tab labels, list and reuse existing tabs, take a fresh snapshot before each action, and retry stale references once with a current ref before reporting a blocker. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aaronmda/openclaw-browser-flows) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only browser automation guidance; no files or code are generated directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
