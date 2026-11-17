## Description:

Generate YAML spell mapping files for OpenClaw Spellbook themed by a topic or URL, using dynamic spell-list discovery and heuristic fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wynnsu](https://clawhub.ai/user/wynnsu)

### License/Terms of Use:


## Use Case:

Developers and agents use Magic Quill to create or refresh themed OpenClaw Spellbook YAML mappings for popular skills. The generated mappings require the separate OpenClaw Spellbook hook before they can be used in agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches broad arbitrary URLs and discovered reference pages.

Mitigation: Use only trusted public topics or URLs, and avoid localhost, intranet, cloud metadata, or credential-bearing pages.

Risk: Install examples use floating npx commands.

Mitigation: Prefer a pinned audited commit or release before installation.

Risk: Generated YAML mappings depend on a separate spellbook hook to affect agent sessions.

Mitigation: Review the spellbook hook before installing it and validate generated files before use.

Risk: The output path can be provided by the user.

Mitigation: Keep --out under spells/ and review the generated YAML before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wynnsu/skills/magic-quill)

## Skill Output:

**Output Type(s):** [configuration, shell commands, guidance]

**Output Format:** [YAML file with console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a themed spell mapping file, usually under spells/, with default top-50 coverage unless a different limit is provided.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
