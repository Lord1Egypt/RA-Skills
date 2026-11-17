## Description:

Integrates OpenClaw agents with a local open-notebook instance for creating, saving, and querying thematic research notebooks using local Ollama models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nantes](https://clawhub.ai/user/nantes)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to connect an OpenClaw agent to a local open-notebook service, then create notebooks, save selected research notes, and query saved knowledge across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may save sensitive, regulated, proprietary, or credential-bearing content into the user's local open-notebook storage.

Mitigation: Use the skill only when local storage, access controls, and retention practices are acceptable; do not submit passwords, API keys, regulated data, or proprietary material unless those controls are approved.

Risk: The skill depends on local open-notebook and Ollama services, notebook IDs, and model IDs being configured correctly.

Mitigation: Confirm the local services are running, verify notebook and model identifiers before use, and review PowerShell commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nantes/skills/open-notebook-integration)
- [Artifact README](artifact/README.md)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with PowerShell function examples and local service configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local open-notebook API usage patterns for notebook creation, note saving, and notebook search.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact Version section)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
