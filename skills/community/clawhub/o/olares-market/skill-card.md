## Description:

Olares Market (olares-cli market) helps agents browse, install, upgrade, uninstall, clone, stop, resume, monitor, upload, and delete Olares Market apps and local Helm chart packages from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olares](https://clawhub.ai/user/olares)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide Olares app-store workflows through `olares-cli market`, including catalog browsing, active app inventory, lifecycle changes, runtime status checks, and local Helm chart upload or deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lifecycle commands such as uninstall, stop, cancel, and cascade actions can interrupt or remove Olares apps.

Mitigation: Confirm the target app name, version, and requested operation before proposing destructive commands, and use status checks or `--watch` when the user needs completion confirmation.

Risk: Deleting a local chart package removes it from the upload bucket and can affect future reinstall workflows.

Mitigation: Confirm the uploaded chart name and version, and distinguish chart deletion from app uninstallation before proposing `olares-cli market delete`.

Risk: Using the wrong market source can produce empty results or target a different catalog than intended.

Mitigation: Verify the source with `market list -a`, source hints, or explicit `-s` values before install, upgrade, or local-chart workflows.

## Reference(s):

- [Olares Market Skill Page](https://clawhub.ai/olares/skills/olares-market)
- [market list / categories / get / status](references/olares-market-list.md)
- [market lifecycle (install / upgrade / uninstall / clone / stop / resume / cancel)](references/olares-market-lifecycle.md)
- [market upload / delete (local chart management)](references/olares-market-charts.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline `olares-cli market` commands and option guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend table or JSON CLI output modes depending on whether the user needs human-readable results or scripted parsing.]

## Skill Version(s):

4.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
