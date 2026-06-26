## Description: <br>
Configures Lean environments, installs external proof skills, runs preflight checks, and guides the workflow for proving downloaded OpenMath Lean theorems locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bennyzhe](https://clawhub.ai/user/bennyzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and theorem-proving engineers use this skill to prepare a downloaded OpenMath Lean workspace, check the local Lean and Mathlib setup, and follow a proof workflow through final build verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can run local commands and optionally install external Lean proof skills. <br>
Mitigation: Use it only for the OpenMath Lean theorem workflow, review the external leanprover/skills source before using npx or auto-install, prefer a project-local skills directory such as .codex/skills, and run preflight only against the intended theorem workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bennyzhe/openmath-lean-theorem) <br>
- [Lean proof skills](https://github.com/leanprover/skills) <br>
- [OpenMath Lean Workspace Preflight](references/preflight.md) <br>
- [OpenMath Lean Proof Playbook](references/proof_playbook.md) <br>
- [Lean Language Specification](references/languages.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to run local Lean, Lake, Elan, Python, npx, and optional git-based installation commands when the user chooses those steps.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
