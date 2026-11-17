## Description:

Operate Mux assets and uploads through an OOMOL-connected account using the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and manage Mux video assets, direct uploads, and playback IDs through their connected account. State-changing and destructive actions require confirmation of the exact effect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the user to execute a remote CLI installer whose contents and effects were not inspected.

Mitigation: Review and install the CLI separately from a verified release, and check its automatic skill synchronization settings before enabling this skill.

Risk: Mux write and destructive actions can change or permanently remove account data.

Mitigation: Confirm the intended Mux account and the exact payload and effect before every write or deletion.

## Reference(s):

- [oo CLI repository (linked by the skill)](https://github.com/oomol-lab/oo-cli)
- [Mux API documentation](https://www.mux.com/docs/core/make-api-requests)
- [Mux homepage](https://www.mux.com)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action responses summarized as natural-language text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may create, update, or delete Mux data; confirm the exact payload and effect before writes or destructive actions.]

## Skill Version(s):

1.0.6 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
