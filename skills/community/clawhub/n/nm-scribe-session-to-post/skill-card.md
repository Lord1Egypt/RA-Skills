## Description: <br>
Converts a Claude Code session into a blog post, case study, or Reddit post. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and developer-relations teams use this skill to turn real Claude Code sessions into publishable engineering blog posts, case studies, social threads, or Reddit posts grounded in session evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated posts may expose credentials, private prompts, internal architecture, customer data, proprietary plans, or other sensitive repository context. <br>
Mitigation: Review every generated draft before publication and remove private or proprietary details. <br>
Risk: Generated posts may contain incorrect or misleading claims about the coding session. <br>
Mitigation: Verify claims against git history, file changes, test output, metrics, and proof-of-work evidence before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-scribe-session-to-post) <br>
- [Clawdis homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scribe) <br>
- [Narrative Structure module](artifact/modules/narrative-structure.md) <br>
- [Reddit Post Format module](artifact/modules/reddit-format.md) <br>
- [Session Extraction Checklist module](artifact/modules/session-extraction.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown prose with optional shell command blocks and concise status fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include word count, verification status, target format, and publication-readiness notes.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
