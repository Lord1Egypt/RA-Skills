## Description: <br>
Formal verification using Lean 4 and the Leanstral labs-leanstral-2603 model for code correctness, protocol verification, algorithm correctness, security property proofs, and other logical theorems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lykeion-dev](https://clawhub.ai/user/lykeion-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to model critical code, algorithms, protocols, and security properties in Lean 4, ask Leanstral to generate proofs, and verify the resulting Lean files with lake. It is most useful for focused correctness claims where a formal specification can be reviewed and compiled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Theorem statements, code, and prompts may be sent to Mistral's API. <br>
Mitigation: Use a dedicated MISTRAL_API_KEY and remove secrets, confidential code, and proprietary protocol details before prompting. <br>
Risk: Generated Lean files are untrusted code and may be compiled on the user's machine. <br>
Mitigation: Review generated Lean files, reject proof holes such as sorry or admit, and run lake builds in a disposable Lean project or sandbox. <br>
Risk: A verified proof only shows that the Lean theorem was proven, not that the theorem matches the user's real-world intent. <br>
Mitigation: Review theorem statements and map each proven theorem back to the intended property before relying on the result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lykeion-dev/leanstral-formal-verification) <br>
- [Mistral Leanstral announcement](https://mistral.ai/news/leanstral) <br>
- [Leanstral model on Hugging Face](https://huggingface.co/mistralai/Leanstral-2603) <br>
- [Mistral Leanstral API documentation](https://docs.mistral.ai/models/leanstral-26-03) <br>
- [Lean 4](https://github.com/leanprover/lean4) <br>
- [Mathlib](https://github.com/leanprover-community/mathlib4) <br>
- [Lean AI leaderboard](https://lean-lang.org/eval/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Lean code, bash commands, API call examples, and verification steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires lake and MISTRAL_API_KEY; generated Lean proofs should be reviewed and compiled before use.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
