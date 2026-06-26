## Description: <br>
Two-agent iterative vibe-coding loop for OpenClaw that uses one sub-agent to generate or revise an app or artifact and a second analyst agent to inspect code, visually preview frontend work, run small functional checks, and feed concrete fixes back until the result matches the target. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rocketship4545-a11y](https://clawhub.ai/user/rocketship4545-a11y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate an iterative generator and visual analyst workflow for UI-heavy apps, prototypes, dashboards, landing pages, and other artifacts where rendered behavior matters. It is intended to improve a result through code review, browser-based visual inspection, functional smoke testing, and targeted revision loops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can direct an agent to edit a project, run local commands, install dependencies, open a browser, and coordinate sub-agents. <br>
Mitigation: Run it on a scoped project or branch and review dependency installs, commands, and proposed changes before relying on the result. <br>
Risk: Browser previews and screenshots used for visual QA can expose secrets, private customer data, tokens, or unrelated logged-in sessions. <br>
Mitigation: Use clean test data and avoid showing secrets, tokens, private data, or unrelated authenticated browser sessions during review. <br>
Risk: If the app cannot launch or visual inspection tools are unavailable, the analyst may be unable to verify rendered behavior. <br>
Mitigation: Treat blocked visual QA as a blocker or caveat rather than acceptance, and provide preview commands, credentials, or alternate inspection paths when appropriate. <br>


## Reference(s): <br>
- [Loop Patterns](references/loop-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/rocketship4545-a11y/match-loop) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance and feedback packets, with code, shell commands, and configuration changes when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Iterative generator and analyst handoffs may include preview instructions, screenshot paths, smoke-test results, prioritized fixes, and acceptance status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
