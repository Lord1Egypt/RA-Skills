## Description: <br>
Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[banalit](https://clawhub.ai/user/banalit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to drive browser workflows through a CLI, using accessibility snapshots and stable element references for navigation, form entry, extraction, session handling, and browser state management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved browser state, cookies, and storage files can grant access to logged-in accounts. <br>
Mitigation: Protect saved auth files, delete them when no longer needed, and use low-privilege or test accounts for automation. <br>
Risk: Browser automation can perform sensitive actions such as purchases, posts, deletions, or account changes. <br>
Mitigation: Require explicit confirmation before executing sensitive workflows and avoid using privileged accounts by default. <br>
Risk: The skill depends on the external agent-browser CLI. <br>
Mitigation: Install agent-browser only from a trusted source and pin the package version where operational stability matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/banalit/luke-agent-browser-clawdbot) <br>
- [agent-browser homepage](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to call the external agent-browser CLI; browser snapshots and command responses may be returned as JSON by that CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
