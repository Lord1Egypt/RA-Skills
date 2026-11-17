## Description:

This skill operates Weights & Biases through an OOMOL-connected account using the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use the skill to inspect and manage Weights & Biases projects, runs, artifacts, reports, and Weave traces through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute an unverified installer and introduce broader agent-skill changes through automatic synchronization.

Mitigation: Review and verify the installer before allowing installation or first run; review automatic skill synchronization and disable it if unwanted.

Risk: Connecting Weights & Biases entrusts OOMOL with provider credentials and requested data; the installer and hosted connector remain unverified.

Mitigation: Review the connection setup and data access before connecting, and connect only when you accept that handling.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Weights & Biases](https://wandb.ai)
- [Weights & Biases API documentation](https://docs.wandb.ai/platform/mcp-server)

## Skill Output:

**Output Type(s):** [Shell commands, API responses, Analysis, Reports]

**Output Format:** [JSON connector requests and responses, with text or Markdown summaries and reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Request and response details vary by action; write actions can create or update Weights & Biases data.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
