## Description:

Import an agent's memory files and scheduled tasks into Klik after review, cleanup, and one-time-code upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengyixu](https://clawhub.ai/user/chengyixu)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to migrate agent memory files and durable scheduled tasks into Klik. It guides the agent through discovery, cleanup, payload validation, user review, and upload using a short-lived import code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive memory or scheduled-task data can be uploaded with metadata that is not fully redacted or previewed.

Mitigation: Review the exact draft payload before submitting, including frontmatter, paths, collector names, and scheduled-task prompts; avoid use when memory may contain credentials, private project names, or personal data until metadata redaction or exact final-payload preview is available.

Risk: Crontab inspection can include system-level scheduled jobs beyond agent memory tasks.

Mitigation: Only consent to crontab inspection when those jobs should be considered for import, and review skipped and included task summaries before upload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chengyixu/skills/klik-import)
- [Agent Skills v1.0 specification](https://agentskills.io/specification)
- [Klik pre-launch page](https://pre.hiklik.ai/?utm_source=github&utm_medium=readme&utm_campaign=kickstarter_prelaunch&utm_content=klik_import_skill_workflow)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands and a JSON import payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a temporary draft payload for validation and upload; final upload requires user confirmation and a 6-digit Klik import code.]

## Skill Version(s):

0.1.0 (source: package.json, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
