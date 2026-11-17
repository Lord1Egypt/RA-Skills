## Description:

CLI tool to find which LLM models run on your local hardware by checking GPU, CPU, and RAM and returning compatible models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsonbuilds](https://clawhub.ai/user/johnsonbuilds)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to select open-weight LLMs that fit local GPU, CPU, RAM, and VRAM constraints. It supports agent workflows, CI/CD compatibility checks, and tradeoff analysis across model families, context lengths, and quantization options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Third-party installation commands can introduce normal supply-chain risk.

Mitigation: Verify that the Homebrew formula, Python package, or GitHub release belongs to the intended project, prefer a specific reviewed version, and check release hashes or signatures where available.

Risk: The tool inspects local hardware details and contacts HuggingFace for model metadata.

Mitigation: Run it only in environments where local hardware inspection and outbound HuggingFace requests are acceptable, and provide HuggingFace credentials only when gated model access is intentionally required.

Risk: VRAM and speed estimates may differ from actual runtime behavior.

Mitigation: Validate selected models on the target machine before relying on the recommendation for deployment or automation.

## Reference(s):

- [Server-resolved ClawHub release page](https://clawhub.ai/johnsonbuilds/skills/llmfit-2)
- [Server-resolved GitHub import](https://github.com/johnsonbuilds/awesome-hermes-skills/tree/main/mlops/llmfit)
- [llmfit GitHub repository](https://github.com/AlexsJones/llmfit)
- [llmfit documentation](https://github.com/AlexsJones/llmfit#readme)
- [llmfit releases](https://github.com/AlexsJones/llmfit/releases)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and tabular CLI output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model compatibility rankings, estimated inference speed, VRAM requirements, and installation or server-mode commands.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
