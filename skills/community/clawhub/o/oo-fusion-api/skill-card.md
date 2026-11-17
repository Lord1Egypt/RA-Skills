## Description:

OOMOL Fusion API (oomol.com). Use this skill for ANY OOMOL Fusion API request — reading, creating, updating, and deleting data. Whenever a task involves OOMOL Fusion API, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill with an OOMOL-connected account to inspect action schemas and run OOMOL Fusion API tasks, including media generation and editing, transcription, OCR, document conversion, search, and file uploads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some media operations may bypass the skill's approval rules.

Mitigation: Have the publisher correct the action classifications and require user confirmation for actions that change data.

Risk: CLI setup runs a remote installer whose local changes were not available for inspection.

Mitigation: Keep CLI setup explicitly user-directed, review the installer and resulting changes, and use a reviewed CLI release.

Risk: Generation and editing requests may incur costs and send content for external processing.

Mitigation: Confirm expected costs and external processing before submitting generation or editing requests.

## Reference(s):

- [OOMOL Fusion API](https://www.oomol.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API results or task status returned by OOMOL Fusion API actions.]

## Skill Version(s):

1.0.10 (source: server-resolved release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
