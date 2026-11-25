## Description:

Helps plan desktop PC builds and upgrades, check component compatibility, and select hardware for gaming, creator work, and local AI using China-market CNY price references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gongyu0918-debug](https://clawhub.ai/user/gongyu0918-debug)

### License/Terms of Use:

MIT-0

## Use Case:

External users planning a desktop PC build or upgrade use the skill to compare components, check compatibility, and size hardware for gaming, creator workloads, and local AI.

### Deployment Geography for Use:

Global; bundled price references cover the China market in CNY.

## Known Risks and Mitigations:

Risk: File-reading and network scope is not declared, and the host runtime’s permission limits were not verified.

Mitigation: Review the requested file and network access against the host’s permission controls before enabling the skill.

Risk: Some responses may be large for workflows with limited output capacity.

Mitigation: Ask for a focused set of components or a concise summary when output size matters.

## Reference(s):

- [PC Build Assistant on ClawHub](https://clawhub.ai/gongyu0918-debug/skills/pc-builder-assistant)
- [Component compatibility guidance](artifact/references/compatibility.md)
- [Pricing guidance](artifact/references/pricing.md)
- [Local model hardware fit guidance](artifact/references/local-model-fit.md)
- [Hugging Face Transformers quantization documentation](https://huggingface.co/docs/transformers/main/en/quantization)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown recommendations with component lists, price summaries, and compatibility guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bundled prices are China-market CNY references with evidence dates; user-provided overlays keep their currencies separate.]

## Skill Version(s):

0.1.57 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
