## Description:

Use AtmoRouter through an OOMOL-connected account to list models and generate chat or message completions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect AtmoRouter model availability and generate chat or message completions through an existing OOMOL connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat and message generation may incur per-token charges and send user-provided content through OOMOL to AtmoRouter.

Mitigation: Require clear authorization and spending limits for generation, and decide which content may be sent before invoking these actions.

Risk: The setup instructions can execute a downloaded CLI installer directly, and external installer behavior is unverified.

Mitigation: Use a reviewed, verified CLI installation and check whether it installs additional agent skills.

## Reference(s):

- [AtmoRouter](https://atmorouter.dev)
- [AtmoRouter Quickstart Documentation](https://atmorouter.dev/docs/quickstart)
- [oo CLI Repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI Installation Guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Generated text and JSON responses, with Markdown usage guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inference responses may incur per-token charges.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
