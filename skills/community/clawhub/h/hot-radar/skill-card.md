## Description:

Tracks multi-platform trending topics, analyzes lifecycle and resonance signals, and produces structured daily hot-topic reports with product-manager-oriented topic suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gold3bear](https://clawhub.ai/user/gold3bear)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, content strategists, and operations teams use this skill to monitor cross-platform trend movement, competitor keywords, AI and finance news, and daily briefing opportunities. It helps an agent collect hot-topic data, cluster related topics, score resonance, identify lifecycle stage, and generate Markdown reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu sync and notification can send collected reports to hard-coded Feishu destinations.

Mitigation: Run without --sync-bitable or --notify until all Feishu app, table, user, and document identifiers are replaced with destinations you control.

Risk: Workspace Feishu tokens or Instagram session cookies may be reused by network features.

Mitigation: Use isolated, purpose-limited credentials and avoid providing reusable personal or production credentials.

Risk: Daily crawls depend on external platform access, platform filtering, and local proxy behavior.

Mitigation: Review enabled platforms and proxy settings before scheduled runs, and verify that fetched sources match the intended monitoring scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gold3bear/skills/hot-radar)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)
- [Google Cloud Console credentials](https://console.cloud.google.com/apis/credentials)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown reports, JSON data archives, terminal status text, and optional Feishu message or table updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are organized by collection date and can include platform-specific trend summaries, resonance scores, lifecycle labels, topic suggestions, and source links.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
