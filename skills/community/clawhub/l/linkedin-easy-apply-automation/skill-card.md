## Description: <br>
Automate LinkedIn Easy Apply searches and applications with Puppeteer/Chromium, a verified resume PDF, remote/job-title filtering, stateful daily reruns, and conservative answer guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ralyodio](https://clawhub.ai/user/ralyodio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI coding and operations agents use this skill to prepare and run repeatable LinkedIn Easy Apply searches from a verified resume PDF. It supports conservative form filling, duplicate avoidance, daily reruns, and concise application reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The automation can submit real LinkedIn applications from a logged-in browser session. <br>
Mitigation: Keep dry-run mode enabled until reviewed, use low scan and apply limits, and require operator approval for unknown required fields or account-security prompts. <br>
Risk: The workflow stores local browser profile, state, and run-history files that may contain personal application context. <br>
Mitigation: Use a dedicated protected browser profile, review logs for personal data, and delete profile and state files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ralyodio/linkedin-easy-apply-automation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript, shell, JSON, and text examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes local state and JSONL log paths for submitted, skipped, and already-seen applications.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
