## Description:

Configures Rocq environments, runs preflight checks, and guides the proving workflow for OpenMath Rocq theorems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shentu-ai](https://clawhub.ai/user/shentu-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare Rocq theorem workspaces, run local preflight checks, complete proofs, and verify that generated OpenMath Rocq theorems are ready for submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask an agent to run local Rocq, dune, grep, and opam commands in theorem workspaces.

Mitigation: Review commands before execution and run them only in the intended theorem workspace.

Risk: Installing opam dependencies or optional companion skills can alter the local proof environment.

Mitigation: Review opam dependencies before installation and add companion skills only deliberately into project-local skill directories.

## Reference(s):

- [Rocq Companion Skills](references/companions.md)
- [Rocq Language Specification](references/languages.md)
- [OpenMath Rocq Proof Playbook](references/proof_playbook.md)
- [ClawHub skill page](https://clawhub.ai/shentu-ai/skills/openmath-rocq-theorems)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash and Rocq code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local Rocq, dune, grep, and opam commands for execution in theorem workspaces.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
