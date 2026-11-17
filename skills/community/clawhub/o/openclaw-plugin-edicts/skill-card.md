## Description:

Edicts injects verified ground-truth facts into agent prompts and exposes configurable tools for reading, searching, and managing edicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mssteuer](https://clawhub.ai/user/mssteuer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this OpenClaw plugin to keep critical facts such as launch dates, naming rules, compliance constraints, and embargoes available in agent context. It is intended for teams that want lightweight ground-truth management without a retrieval stack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed artifact may not match the plugin artifact users install.

Mitigation: Install only a pinned, matching artifact with provenance or complete an OpenClaw plugin source review before use.

Risk: Persisted edicts can place incorrect or untrusted content into future agent prompt context.

Mitigation: Keep write tools disabled unless writers are trusted, prefer read-only tool whitelists, set autoSave false when persistence is not intended, and review imported edict files before use.

Risk: Dependency or artifact drift can change runtime behavior after review.

Mitigation: Update flagged dependencies and re-review the exact package version before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mssteuer/skills/openclaw-plugin-edicts)
- [Edicts documentation](https://edicts.ai)
- [OpenClaw plugin package](https://www.npmjs.com/package/openclaw-plugin-edicts)
- [Core library package](https://www.npmjs.com/package/edicts)
- [API reference](https://edicts.ai/docs/reference/api/)
- [CLI reference](https://edicts.ai/docs/reference/cli/)
- [OpenClaw integration guide](https://edicts.ai/docs/integrations/openclaw/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Prompt context text with optional Markdown or JSON renderings, plus CLI and tool responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can persist YAML or JSON edict files when write tools and autoSave are enabled.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
