## Description: <br>
Mobilerun lets agents control and automate connected Android devices through screenshots, UI state, taps, swipes, text entry, app management, and task execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnmalek312](https://clawhub.ai/user/johnmalek312) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and operators use Mobilerun to test Android apps, automate mobile workflows, and perform phone-control tasks on personal or cloud Android devices. Users should give precise instructions because the skill can operate live apps and device screens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent live visibility into and control over a connected Android device. <br>
Mitigation: Install only when live device control is intended, give precise task instructions, and disconnect the Portal app or revoke Accessibility permission when finished. <br>
Risk: Broad requests involving messages, public posts, purchases, banking, crypto, or account settings can expose sensitive data or cause irreversible actions. <br>
Mitigation: Avoid broad requests in these areas and require explicit confirmation before irreversible or high-impact actions. <br>
Risk: Screenshots and UI tree data can contain personal information visible on the device screen. <br>
Mitigation: Use screen data only for the current task, do not share it beyond the user, and never display or log MOBILERUN_API_KEY. <br>
Risk: Cloud devices consume credits while they are running. <br>
Mitigation: Terminate cloud devices after tasks complete and wait for queued or running tasks to finish before termination. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/johnmalek312/mobilerun) <br>
- [Security & Privacy](references/security.md) <br>
- [Setup & Billing](references/setup-and-billing.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Use Cases](references/use-cases.md) <br>
- [Changelog](references/changelog.md) <br>
- [Mobilerun API](https://api.mobilerun.ai/v1) <br>
- [Mobilerun API Keys](https://cloud.mobilerun.ai/api-keys) <br>
- [Mobilerun Billing](https://cloud.mobilerun.ai/billing) <br>
- [Droidrun Portal Download](https://droidrun.ai/portal) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline curl commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MOBILERUN_API_KEY plus curl and jq; may produce device actions through the Mobilerun API.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
