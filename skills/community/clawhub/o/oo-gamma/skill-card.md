## Description:

Use Gamma through an OOMOL-connected account to generate content from text or templates and inspect generation jobs, folders, and themes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Gamma users can create content from text or templates and check generation status, folders, and themes through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup calls for running a remote installer that the security review could not verify, leaving its local changes uncertain.

Mitigation: Review the CLI installation separately, prefer a pinned and verified release, and inspect the installer's expected changes before setup.

Risk: Automatic bundled-skill synchronization could change installed skills during setup.

Mitigation: Review or disable synchronization before first use.

Risk: Gamma requests and generation payloads pass through OOMOL.

Mitigation: Connect only the intended account and confirm the payload before sending it.

## Reference(s):

- [Gamma](https://gamma.app)
- [Gamma API documentation](https://developers.gamma.app/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Text, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and connector responses, summarized in text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation actions may return asynchronous job status and result URLs.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
