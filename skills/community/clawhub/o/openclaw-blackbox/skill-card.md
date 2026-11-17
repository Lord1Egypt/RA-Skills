## Description:

OpenClaw Blackbox CLI inspects failed, stalled, expensive, or unusual OpenClaw agent runs from local disk evidence; lists sessions and failures; finds the session behind a request; and generates terminal, Markdown, JSON, or HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shan8851](https://clawhub.ai/user/shan8851)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect local OpenClaw run evidence, triage failed or suspicious runs, find sessions related to requests, and produce deterministic debugging reports without relying on hidden LLM calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned third-party npm CLI.

Mitigation: Install only after reviewing or pinning the npm package and confirming trust in the package publisher.

Risk: The CLI reads local OpenClaw session history that may contain sensitive prompts, tool results, URLs, and paths.

Mitigation: Inspect explicit sessions when possible, avoid broad all-agent scans unless needed, and limit access to environments where local session data is appropriate to review.

Risk: Generated reports can write sensitive debugging details to disk or open them in external viewers.

Mitigation: Review Markdown, JSON, HTML, and terminal reports before sharing them or opening them outside the trusted environment.

## Reference(s):

- [OpenClaw Blackbox ClawHub page](https://clawhub.ai/shan8851/skills/openclaw-blackbox)
- [shan8851 publisher profile](https://clawhub.ai/user/shan8851)
- [OpenClaw Blackbox npm package](https://www.npmjs.com/package/@shan8851/blackbox)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, HTML, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI reports may be terminal text, Markdown, JSON, or HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can include prompts, tool arguments and results, URLs, and local paths; review generated reports before sharing.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
