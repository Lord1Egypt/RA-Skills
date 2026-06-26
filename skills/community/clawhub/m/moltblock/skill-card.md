## Description: <br>
Verification gating for AI-generated artifacts. Policy checks to catch dangerous patterns before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meshailabs](https://clawhub.ai/user/meshailabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run policy checks on AI-generated artifacts before execution, especially for tasks involving destructive operations, credential access, network activity, file writes, or other elevated-risk behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a selected LLM provider key for cloud-backed verification. <br>
Mitigation: Use a limited-scope or dedicated API key and install only when comfortable running an npm CLI with that key. <br>
Risk: Verification output is best-effort and may miss unsafe or misleading artifact behavior. <br>
Mitigation: Review generated artifact fields before trusting them, and keep human review in the execution path for high-risk tasks. <br>
Risk: The artifact's security wording says policy checks only, while server security guidance says this understates runtime behavior because provider calls can generate artifacts. <br>
Mitigation: Treat the policy-checks-only statement as incomplete and review the tool's generated artifact fields and provider behavior before use. <br>


## Reference(s): <br>
- [Moltblock Repository](https://github.com/moltblock/moltblock) <br>
- [Moltblock Configuration Documentation](https://github.com/moltblock/moltblock#configuration) <br>
- [moltblock npm Package](https://www.npmjs.com/package/moltblock) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON verification results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a configured LLM provider API key; falls back to a local LLM endpoint when no cloud provider key is set.] <br>

## Skill Version(s): <br>
0.11.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
