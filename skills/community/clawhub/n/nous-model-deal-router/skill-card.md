## Description:

Use when choosing best-value Nous Portal models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sknewcomb](https://clawhub.ai/user/sknewcomb)

### License/Terms of Use:

MIT

## Use Case:

Developers and Hermes Agent users use this skill to compare current Nous Portal model pricing, promotions, and capability fit for coding, research, routine agentic work, and other workloads. It recommends one best-value model plus one lower-cost alternative and requires explicit approval before changing any model setting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing from a mutable main-branch URL can make the installed skill differ from the reviewed release.

Mitigation: Prefer a ClawHub-reviewed release, pinned commit, or checksum-verified copy before installation.

Risk: Model recommendations can become stale when Nous Portal pricing, promotions, or availability changes.

Mitigation: Refresh live Portal information and rely on visible current pricing or promotion evidence before recommending a model.

Risk: A model default or active-session model could be changed without enough user intent.

Mitigation: Require explicit approval for the exact proposed model and verify the resulting provider and model after persistent changes.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/sknewcomb/nous-model-deal-router)
- [ClawHub skill page](https://clawhub.ai/sknewcomb/skills/nous-model-deal-router)
- [Hermes Agent](https://github.com/NousResearch/hermes-agent)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline text and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations depend on current Nous Portal pricing and require explicit approval before model changes.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
