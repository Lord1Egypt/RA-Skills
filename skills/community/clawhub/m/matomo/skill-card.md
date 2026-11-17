## Description:

Query, analyze, and manage Matomo Analytics with API integration, custom reports, and goal tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, site owners, and analytics operators use this skill to connect an agent to their own Matomo instance, query traffic and conversion metrics, and generate human-readable dashboards or recurring reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Matomo API tokens can be exposed through command lines, logs, shell history, or chat if pasted directly into curl examples.

Mitigation: Use a dedicated least-privileged token stored in an environment variable or system keychain, reference it indirectly, and avoid pasting real tokens into chat or shell commands.

Risk: Local files under ~/matomo/ may contain site names, site IDs, reporting priorities, templates, and cached analytics context.

Mitigation: Treat ~/matomo/ as sensitive workspace data, keep credentials out of these files, and review stored context before sharing logs or exports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/matomo)
- [Skill homepage](https://clawic.com/skills/matomo)
- [Matomo API Reference](artifact/api.md)
- [Setup](artifact/setup.md)
- [Memory Template](artifact/memory-template.md)
- [Report Templates](artifact/reports.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, API Calls, Analysis]

**Output Format:** [Markdown guidance with Matomo API query patterns, shell command examples, report templates, and analytics summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local configuration under ~/matomo/ and user-controlled Matomo API credentials by secure reference.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata, released 2026-02-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
