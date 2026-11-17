## Description:

Knowledge Curator fetches user-approved links, summarizes and categorizes the content, stores it as a local Markdown knowledge base, and supports search and management commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayuyang-study](https://clawhub.ai/user/mayuyang-study)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to save web and platform links into a structured local knowledge base, then search, list, view, delete, export, and review the stored entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches arbitrary user-provided URLs, which can expose private or internal network destinations if URL handling is not constrained.

Mitigation: Validate destination URLs, block private and internal address ranges, cap response sizes, and run the skill in an isolated environment without internal network access.

Risk: The skill writes and deletes persisted knowledge-base files, and weak validation could affect unintended paths or remove important entries.

Mitigation: Allowlist knowledge-base category paths, normalize paths before file operations, and require clear user confirmation before deleting entries.

Risk: Saved links and fetched page content may contain sensitive URL parameters or private information.

Mitigation: Redact sensitive URL parameters, ask for confirmation before saving sensitive links, and avoid granting the skill access to sensitive local files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mayuyang-study/skills/knowledge-curator)
- [README](artifact/README.md)
- [Quickstart](artifact/QUICKSTART.md)
- [Examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown files, text command responses, JSON indexes, and optional Markdown, JSON, or CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores fetched content under a local knowledge-base directory and maintains an index.json file for search and management operations.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
