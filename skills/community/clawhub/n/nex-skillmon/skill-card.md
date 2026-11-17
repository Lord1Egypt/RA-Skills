## Description:

Nex Skillmon helps OpenClaw users monitor installed skills, track estimated API costs, detect stale or flagged skills, check for updates, and export skill health reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexaiguy](https://clawhub.ai/user/nexaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and teams managing multiple OpenClaw skills use this skill to inventory their skill ecosystem, review health and usage signals, estimate costs, identify stale or flagged skills, and generate JSON or Markdown reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installed skill names, skill paths, usage data, and local configuration values may be sensitive.

Mitigation: Review the skill before installing or running it, especially on shared machines or systems with sensitive skill metadata.

Risk: Update and security-check commands may make outbound requests to api.clawhub.dev.

Mitigation: Use those commands only when outbound ClawHub requests are acceptable for the environment.

Risk: Scanning skill directories that contain symlinks or unexpected paths can weaken filesystem boundaries.

Mitigation: Point SKILLS_BASE_DIR only at intended skill directories and inspect shared or symlink-heavy directories before scanning.

Risk: Local configuration files may expose secrets if users place credentials in this tool's config.

Mitigation: Do not store secrets in Nex Skillmon configuration values.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nexaiguy/skills/nex-skillmon)
- [Publisher profile](https://clawhub.ai/user/nexaiguy)
- [Nex AI homepage](https://nex-ai.be)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal text, Markdown summaries, JSON exports, and Markdown report exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local skill metadata and usage records, store monitoring data under the user's home directory, and call ClawHub update or security endpoints when those commands are used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
