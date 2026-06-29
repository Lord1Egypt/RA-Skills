## Description: <br>
Lean Proof To Code Translator - C Rust Wasm starts asynchronous AgentPMT remote tool calls that convert supported Lean proof archives into C, Rust, or Wasm artifacts and can verify generated bundles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to invoke AgentPMT-hosted Lean proof export workflows, generate C, Rust, or Wasm deliverables from supported LeanCP archives, and verify generated bundles for audit or release review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes priced AgentPMT remote actions that require account setup and may consume credits. <br>
Mitigation: Confirm the request is specifically for Lean proof export or verification and check credit impact before calling generate, verify, or polling actions. <br>
Risk: Unsupported or overbroad Lean archives can fail the workflow or expose source content beyond the intended task. <br>
Mitigation: Review the archive before upload and include only source-only Lean files under UserProofs/ that build the selected CProgramDecl entry symbol. <br>
Risk: Generated targets have different maturity and safety profiles, including unsafe pointer semantics in Rust and a more restrictive preview-grade Wasm path. <br>
Mitigation: Select the target deliberately, inspect generated artifacts, and use the verify action or verification bundle before shipping or publishing outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/lean-proof-to-code-translator-c-rust-wasm) <br>
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/lean-to-code-translator-w-proof-c-rust-wasm) <br>
- [Lean input tutorial](https://www.agentpmt.com/docs/tutorials/write-lean-input-for-code-generation) <br>
- [Lean proof code generation example archive](https://www.agentpmt.com/downloads/lean-proof-code-generation-example.zip) <br>
- [Action schema](schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and generated code artifact references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote actions return JSON task state and artifact references; generated targets are c, rust, or wasm.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
