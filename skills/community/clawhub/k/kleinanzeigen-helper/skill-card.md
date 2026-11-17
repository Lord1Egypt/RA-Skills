## Description:

Manage Kleinanzeigen listings through the KleinClaw OpenClaw plugin and embedded miniclaw runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilyazar](https://clawhub.ai/user/ilyazar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to draft, verify, publish, update, download, extend, or delete Kleinanzeigen listings through configured KleinClaw tools while keeping account-changing actions scoped and confirmed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external KleinClaw plugin that can control configured listing workspaces and live Kleinanzeigen listing actions.

Mitigation: Install and enable KleinClaw only from a trusted source, keep adRoots narrow, and verify the plugin before use.

Risk: Publishing, updating, extending, downloading, or deleting listings can change live Kleinanzeigen account state.

Mitigation: Review the exact listing scope and require explicit user confirmation before any mutating action.

Risk: Credentials, browser profiles, cookies, and configuration files may contain sensitive account data.

Mitigation: Keep credentials and config files out of chat and report only sanitized browser, configuration, and tool results.

## Reference(s):

- [Kleinanzeigen Helper Skill](https://clawhub.ai/ilyazar/skills/kleinanzeigen-helper)
- [KleinClaw Plugin](https://clawhub.ai/plugins/kleinclaw)
- [Prerequisites / Install](artifact/references/install.md)
- [Non-negotiables](artifact/references/non-negotiables.md)
- [Workflow](artifact/references/workflow.md)
- [Ad Authoring](artifact/references/ad-authoring.md)
- [Draft Publish Preflight](artifact/references/draft-publish-preflight.md)
- [Listing Discovery and Scoping](artifact/references/listing-discovery-scoping.md)
- [Browser Behaviour](artifact/references/browser-behaviour.md)
- [Publish Result Caveats](artifact/references/publish-result-caveats.md)
- [Tool Selection](artifact/references/tool-selection.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured tool-selection instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports sanitized results only and requires explicit user confirmation before mutating live Kleinanzeigen listings.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
