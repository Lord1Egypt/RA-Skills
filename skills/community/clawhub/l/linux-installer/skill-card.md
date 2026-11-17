## Description:

Installs, launches, and uninstalls Linux desktop apps by resolving the safest supported source first, then running a local helper CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baladoodle](https://clawhub.ai/user/baladoodle)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and Linux administrators use this skill to resolve, install, launch, and uninstall Linux desktop apps through preferred package sources while seeing explicit warnings for community, unreviewed, or manual fallback paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run local package-manager commands, including sudo-backed installs, removals, and service setup.

Mitigation: Use it only when the operator is comfortable with local package-manager changes, review the resolved command, and require explicit user confirmation before execution.

Risk: Security evidence flags AUR behavior that may install community-controlled packages with reduced safeguards.

Mitigation: Avoid AUR installs until AUR candidates are always labeled community or unreviewed, require separate confirmation, and avoid --noconfirm.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baladoodle/skills/linux-installer)
- [README](artifact/README.md)
- [Catalog guide](artifact/CATALOG_GUIDE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source labels, exact install, launch, and uninstall commands, and warnings for community, unreviewed, or manual paths.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
