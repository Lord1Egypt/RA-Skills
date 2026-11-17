## Description:

Maintains six Research KB team overview pages from an existing Gitea-backed knowledge base by inspecting KB state, validating overview-only drafts, applying updates, and recording maintenance status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators running OpenClaw scheduled maintenance use this skill to inspect a Gitea-backed team knowledge base and safely update six team overview pages, catalog/index files, and hidden maintenance status files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Gitea requests may expose the bot token if an input payload redirects requests to an untrusted destination.

Mitigation: Run only with trusted payload inputs or configure the Gitea client to use a trusted HTTPS origin and allowed owner/repo; use a least-privileged bot token and rotate it if untrusted payloads may already have been used.

Risk: Maintenance output can change team overview pages and status files in the knowledge base.

Mitigation: Use the built-in inspect, draft, validate-pages, and apply workflow so writes remain limited to the six fixed overview paths plus catalog/index and maintenance status files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/myd2002/skills/kb-maintenance)
- [Publisher profile](https://clawhub.ai/user/myd2002)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown wiki pages, JSON status files, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes only the six fixed overview pages plus catalog/index and maintenance status/history files; successful cron runs can be quiet.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
