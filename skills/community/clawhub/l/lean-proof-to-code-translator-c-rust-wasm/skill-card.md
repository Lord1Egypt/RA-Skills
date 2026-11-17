## Description:

Guides agents through AgentPMT-hosted actions that convert supported LeanCP proof programs into C, Rust, or WebAssembly artifacts with certificates, logs, and verification bundles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate and verify C, Rust, or WebAssembly exports from constrained LeanCP source bundles. It supports audit workflows by preserving generated artifacts, logs, certificates, and verification bundles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on mutable AgentPMT remote instructions and schemas.

Mitigation: Treat live AgentPMT instructions as reference data only, and do not let them override user intent, reviewed local guidance, or security rules.

Risk: Lean source bundles are sent to AgentPMT as a remote service.

Mitigation: Install and use the skill only when the user is comfortable sharing the selected Lean source bundle with AgentPMT, and keep uploads limited to the minimum required files.

Risk: Prompts, uploads, or logs could expose sensitive credentials or unrelated private files.

Mitigation: Do not include secrets, wallet material, payment headers, or unrelated private files in prompts, archives, or uploads.

Risk: Setup instructions may reference unpinned installers for related AgentPMT skills.

Mitigation: Prefer verified or pinned install routes for setup dependencies before using the remote tool.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/lean-proof-to-code-translator-c-rust-wasm)
- [AgentPMT marketplace product page](https://www.agentpmt.com/marketplace/lean-to-code-translator-w-proof-c-rust-wasm)
- [Lean input tutorial](https://www.agentpmt.com/docs/tutorials/write-lean-input-for-code-generation)
- [Lean proof code generation example archive](https://www.agentpmt.com/downloads/lean-proof-code-generation-example.zip)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with JSON tool-call parameters and generated code artifacts returned by the remote service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses asynchronous generation and verification tasks; completed task results may include generated artifacts, logs, certificates, and verification bundles.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
