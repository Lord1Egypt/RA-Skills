## Description: <br>
Records browser sessions via Playwright and converts video to GIF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to record automated browser interactions with Playwright and create WebM or GIF assets for web UI tutorials, demos, and documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser recordings may capture credentials, tokens, customer data, or internal dashboard content visible in the page. <br>
Mitigation: Use test accounts or sanitized demo data, avoid sensitive pages, and review videos and GIFs before sharing. <br>
Risk: Generated recordings can be misleading if the Playwright spec is flaky, too fast, or ends before the page reaches the intended state. <br>
Mitigation: Use explicit waits, stable viewports, and final pauses, then verify that the output video exists and has non-zero size. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-scry-browser-recording) <br>
- [Scry source plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scry) <br>
- [modules/spec-execution.md](artifact/modules/spec-execution.md) <br>
- [modules/video-capture.md](artifact/modules/video-capture.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with TypeScript configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to produce Playwright recording steps, video output paths, and optional GIF conversion instructions.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
