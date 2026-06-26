## Description: <br>
MOOC automation tool for completing course video learning, detecting chapter status, and waiting for video playback to finish. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonylemon](https://clawhub.ai/user/tonylemon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or developers use this skill to configure and run Playwright-based automation for MOOC course videos, including chapter detection, playback monitoring, progress recovery, and learning reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The automation can act on a logged-in MOOC account and may conflict with platform rules or user expectations. <br>
Mitigation: Install and run it only when the platform permits this automation, restrict the configured course URLs, and use an isolated browser profile. <br>
Risk: Broad browser control and the automation-hiding flag can reduce transparency during the handoff window. <br>
Mitigation: Avoid unrelated tabs while the script runs and remove the automation-hiding flag unless explicitly authorized. <br>
Risk: Local progress and report files may retain course activity data. <br>
Mitigation: Review and delete learning-progress.json and learning-report.json when they are no longer needed. <br>


## Reference(s): <br>
- [MOOC Learner Detailed Documentation](references/README.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript configuration snippets and shell commands; runtime artifacts are JSON progress and report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The documented script writes learning-progress.json and learning-report.json while operating a local Chrome browser session.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
