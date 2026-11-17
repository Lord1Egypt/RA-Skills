## Description:

Prompt Library Manager stores, searches, versions, tags, and reuses prompt templates across OpenClaw sessions and agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevojarvisai-star](https://clawhub.ai/user/stevojarvisai-star)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, teams, and OpenClaw agent users use this skill to store, search, version, tag, reuse, import, and export prompt templates across sessions and agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The prompt library persists locally across sessions and may contain sensitive prompt content.

Mitigation: Avoid storing secrets or confidential data in prompt templates, and review local and exported prompt library files before sharing them.

Risk: Import, --from-file, export, and --workspace accept user-selected paths that may read from or write to sensitive or system locations.

Mitigation: Use a dedicated workspace path, avoid sensitive or system paths, and inspect imported and exported files before relying on or distributing them.

Risk: Deleting a prompt is immediate and does not enforce a confirmation or recovery workflow.

Mitigation: Export or back up the library before deletes, and verify the prompt name before running delete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stevojarvisai-star/skills/prompt-library-manager)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [CLI text, JSON, Markdown exports, and filled prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores prompt library data locally in memory/prompt-library.json under the configured OpenClaw workspace.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
