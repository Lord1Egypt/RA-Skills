## Description:

Provides guidance for using Lean 4, Mathlib, and Mistral AI's Leanstral model to generate and verify formal proofs for code correctness, algorithms, protocols, and security properties.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lykeion-dev](https://clawhub.ai/user/lykeion-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to model critical code behavior, protocols, algorithms, and security properties as Lean 4 theorems, ask Leanstral to generate proofs, and compile those proofs for mechanical checking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Theorem statements, code, or protocol details may be sent to Mistral's API during proof generation.

Mitigation: Do not include private code, secrets, proprietary protocol details, or other confidential material in prompts.

Risk: Model-generated Lean files are untrusted code and the security evidence flags host compilation guidance as suspicious.

Mitigation: Compile generated Lean files only in a disposable, isolated environment, verify the exact generated file is checked, and reject proof holes such as sorry or admit before building.

Risk: A mechanically valid proof only establishes the theorem that was written, not whether that theorem captures the user's real-world intent.

Mitigation: Review theorem statements and specifications before relying on successful Lean compilation as assurance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lykeion-dev/skills/leanstral-formal-verification)
- [Mistral Leanstral announcement](https://mistral.ai/news/leanstral)
- [Leanstral model card](https://huggingface.co/mistralai/Leanstral-2603)
- [Mistral Leanstral API docs](https://docs.mistral.ai/models/leanstral-26-03)
- [Mistral API keys](https://console.mistral.ai/api-keys)
- [Lean 4](https://github.com/leanprover/lean4)
- [Mathlib](https://github.com/leanprover-community/mathlib4)
- [Elan Lean version manager](https://github.com/leanprover/elan)
- [Lean AI evaluation](https://lean-lang.org/eval/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Lean, shell, Python, and API request snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a Mistral API key and local Lean 4 project setup before generated proofs can be checked.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
