## Description:

One-stop Minecraft mod ecosystem intelligent management tool with 15 features including mod search, environment setup, Mixin conflict scanning, crash fix, translation, migration assessment, save sync, authorization management, online payment system, admin dashboard, and automated business reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liang030214](https://clawhub.ai/user/liang030214)

### License/Terms of Use:

MIT-0

## Use Case:

Minecraft players, mod developers, and modpack creators use this skill to find and assess mods, configure environments, diagnose crashes and conflicts, translate or repack resources, and manage saves. It provides recommendations, repair guidance, and automation for common mod-management tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Save-sync restoration and resource repacking may affect valuable saves or files, and shared sync folders may be modifiable by others.

Mitigation: Test with disposable game copies and separate backups; trust everyone with access to the sync folder and inspect replacement resources before use.

Risk: Generated reports can contain injected scripts.

Mitigation: Treat generated reports as untrusted content; sanitize them before sharing or displaying them as HTML.

Risk: Offline settings do not prevent all network requests.

Mitigation: Do not rely on --offline as a network-blocking control, and leave the local API disabled unless needed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, Files]

**Output Format:** [Text or Markdown analysis and guidance, shell commands, and generated or modified HTML and Minecraft files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some features read or modify local game files and may require network access.]

## Skill Version(s):

1.0.4 (source: skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
