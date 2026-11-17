## Description:

Operate ImageKit through an OOMOL-connected account for reading, creating, updating, and deleting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search ImageKit assets, inspect file and media metadata, check cache-purge status, request cache purges, or delete file versions through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute an unverified installer, and the installed CLI version is not verified by the available evidence.

Mitigation: Review and install the CLI separately before use, and verify the installer and resulting version.

Risk: CLI setup or invocations may make undisclosed changes to other agents’ skill directories.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 for CLI invocations and review any proposed skill-directory changes.

Risk: The skill exposes destructive ImageKit actions that permanently delete file versions or submit cache purge requests.

Mitigation: Require explicit approval for each destructive action after reviewing its exact target, payload, and effect.

## Reference(s):

- [ImageKit Documentation](https://imagekit.io/docs/api-overview)
- [ImageKit](https://imagekit.io)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON payloads and JSON responses, plus brief operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response fields vary by ImageKit action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
