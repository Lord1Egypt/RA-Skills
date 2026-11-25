## Description:

Search UberLLM data, list available models, and request chat completions through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users use this skill to list UberLLM models or request chat completions through an already connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI setup points to a remote installer whose contents were not assessed by the partial scan.

Mitigation: Avoid installation until the CLI setup is clearly explained and the installer can be independently checked.

Risk: Paid inference may incur charges, and the data sent by that action is unclear.

Mitigation: Before running a chat completion, confirm whether it incurs charges and what data it sends.

## Reference(s):

- [UberLLM documentation](https://uberllm.dev/docs/quickstart)
- [UberLLM](https://uberllm.dev)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Text or JSON returned by the UberLLM connector]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chat completion requests are billed; model-list results include model metadata.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
