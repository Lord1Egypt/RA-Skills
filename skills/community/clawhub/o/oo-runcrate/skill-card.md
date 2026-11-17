## Description:

Use Runcrate through the oo CLI to list available models and submit chat-completion or message inference requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Runcrate users use this skill to inspect available models and submit chat or message inference requests through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted inference content can result in charges.

Mitigation: Review and approve the inference content and charges before use, and set a spending limit.

Risk: The setup instructions run a downloaded installer when the oo CLI is missing.

Mitigation: Install the CLI separately from a reviewed, verified release instead of running a downloaded script in response to a missing-command error.

## Reference(s):

- [Runcrate API documentation](https://www.runcrate.ai/docs/models/overview)
- [Runcrate homepage](https://www.runcrate.ai)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI install guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Generated text or JSON responses from Runcrate actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inference requests are billed; listing models does not run inference.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
