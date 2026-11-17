## Description:

Capture OpenRouter Rankings (all Categories scenarios + page sections), create Feishu doc with screenshots and sales summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neymar011ren](https://clawhub.ai/user/neymar011ren)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and operations teams use this skill to capture the OpenRouter rankings page, summarize model trends across business scenarios, and share the resulting daily digest in Feishu. Developers or automation maintainers can run the scripted workflow on a schedule after configuring Chromium and Feishu tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The browser capture workflow can be pointed at arbitrary URLs while Chromium is launched without sandboxing.

Mitigation: Allowlist https://openrouter.ai/rankings, restrict network egress, and avoid no-sandbox Chromium execution where possible.

Risk: Automated Feishu document creation can distribute incomplete or unreviewed ranking reports.

Mitigation: Keep screenshot validation as a required gate, validate manifest file paths before upload, and review the generated document before broad sharing.

## Reference(s):

- [OpenRouter Rankings](https://openrouter.ai/rankings)
- [ClawHub skill page](https://clawhub.ai/neymar011ren/skills/openrouter-rankings-screenshot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, plain-text chat summary, PNG screenshots, JSON manifest, and Feishu document link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshots and summaries are generated only after validation checks pass.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
