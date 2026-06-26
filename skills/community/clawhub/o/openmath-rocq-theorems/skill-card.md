## Description: <br>
Configures Rocq environments, runs preflight checks, and guides the proving workflow for OpenMath Rocq theorems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shentu-ai](https://clawhub.ai/user/shentu-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare Rocq theorem workspaces, validate local tooling, complete OpenMath Rocq proofs, and verify proofs before submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide the agent to run local Rocq, dune, grep, and opam commands in a theorem workspace. <br>
Mitigation: Run it only in the intended theorem workspace and review proposed commands before execution. <br>
Risk: Dependency installation through opam can change the active proof environment. <br>
Mitigation: Review the project opam file first and prefer a dedicated opam switch when practical. <br>
Risk: An incomplete proof could be mistaken for a finished submission. <br>
Mitigation: Require a passing dune build or Rocq compile and confirm no admit or Admitted markers remain before submission. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shentu-ai/openmath-rocq-theorems) <br>
- [Rocq Companion Skills](references/companions.md) <br>
- [Rocq Language Specification](references/languages.md) <br>
- [OpenMath Rocq Proof Playbook](references/proof_playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and Rocq proof snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local Rocq, dune, grep, and opam commands for execution in the theorem workspace.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports v1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
