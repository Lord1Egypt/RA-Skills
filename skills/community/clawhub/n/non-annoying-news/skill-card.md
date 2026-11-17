## Description:

Create, configure, and render a source-grounded personal newspaper or news digest from user-provided and configured sources, with onboarding gates before personal issues, recurring schedules, cron jobs, or external delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iret77](https://clawhub.ai/user/iret77)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to set up and produce source-grounded personal newspapers or news digests from URLs, saved items, feeds, newsletters, exports, and web research. It supports first-run onboarding, source configuration, editorial QA, HTML/PDF rendering, and recurring issue setup with explicit consent gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional browser, X/Twitter, mailbox, delivery, or scheduling access can expose personal data or trigger future actions if enabled without clear consent.

Mitigation: Enable those sources and actions only after explicit user approval, keep credentials configured locally, and use the Personalization Gate before creating personal issues, recurring jobs, cron entries, or external delivery.

Risk: Rendering arbitrary or untrusted HTML can carry content and browser-rendering risks.

Mitigation: Render only reviewed or sanitized HTML, run with network and JavaScript disabled when possible, and use reviewed, pinned renderer dependencies.

Risk: Saved bookmarks, reading-list entries, and social posts are intent signals, not verified factual sources.

Mitigation: Fetch and read linked content where possible, mark inaccessible or metadata-only items, and state source boundaries in the issue.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iret77/skills/non-annoying-news)
- [Onboarding Guide](artifact/references/onboarding.md)
- [Local Configuration](artifact/references/config-schema.md)
- [Source and Signal Adapters](artifact/references/source-adapters.md)
- [Editorial Standard](artifact/references/editorial-standard.md)
- [Layout and Render QA](artifact/references/layout-and-render-qa.md)
- [Design Presets and Personalization](artifact/references/design-presets.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON configuration, source manifests, HTML/PDF issue artifacts, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local HTML, PDF, and PNG preview files when renderer dependencies are available; external delivery and scheduling require explicit user approval.]

## Skill Version(s):

0.2.1 (source: server release evidence and SKILL.md package version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
