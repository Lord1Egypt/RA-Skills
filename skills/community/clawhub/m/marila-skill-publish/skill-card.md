## Description:

Guides agents through publishing and updating OpenClaw skills on ClawHub, including GitHub Release synchronization, versioning, pre-release checks, and common ClawHub publishing fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aliramw](https://clawhub.ai/user/aliramw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this documentation skill to prepare, publish, troubleshoot, and update OpenClaw skills on ClawHub while keeping GitHub releases and metadata aligned.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual publishing guidance can lead users to extract local ClawHub tokens from configuration files.

Mitigation: Prefer the official clawhub CLI publishing path and avoid manual token extraction unless a trusted operator explicitly approves the fallback.

Risk: Broad file uploads or blanket git add -A staging can include unintended files or secrets.

Mitigation: Use an explicit manifest or explicit staging, then run secret and file-scope checks before publishing.

Risk: Writing directly to ~/.openclaw/workspace/skills can alter later agent behavior.

Mitigation: Treat workspace skill writes as administrative actions and perform them only in trusted environments after review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aliramw/skills/marila-skill-publish)
- [ClawHub metadata homepage](https://github.com/aliramw/dingtalk-ai-table)
- [ClawHub review checklist](references/clawhub-review-checklist.md)
- [ClawHub skill marketplace](https://clawhub.ai/skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local tools declared by metadata: clawhub, git, and gh.]

## Skill Version(s):

1.0.8 (source: frontmatter, package.json, CHANGELOG, server release metadata; released 2026-03-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
