## Description:

Packages an existing local HTML/CSS/JavaScript site or built frontend into a self-contained Electron desktop application for macOS or Windows without deploying it to a server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ully](https://clawhub.ai/user/ully)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert local static sites or built frontend projects into offline Electron desktop apps, with guidance for icons, signing, platform targets, and local SQLite storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Projects containing secrets or broad source trees can be unintentionally bundled, especially when fallback packaging paths are used.

Mitigation: Prefer electron-builder with an explicit files allowlist, inspect final bundle contents before distribution, and avoid packaging secrets.

Risk: The cached macOS fallback can trust a supplied Electron archive without enforcing integrity checks.

Mitigation: Use the cached runtime only when the archive exactly matches the intended Electron version and architecture and has been independently verified.

Risk: Remote APIs, OAuth, CDN assets, or server databases cannot be made offline just by packaging local web files.

Mitigation: Identify online dependencies during inspection and decide connectivity, credential storage, and offline behavior before delivery.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ully/skills/html2app)
- [Packaging Matrix](artifact/references/packaging-matrix.md)
- [Packaging Test Cases](artifact/references/test-cases.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and code/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also result in local Electron project files and desktop application artifacts when executed in a target project.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
