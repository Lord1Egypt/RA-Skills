## Description:

Configures Lean environments, installs external proof skills, runs preflight checks, and guides the workflow for proving downloaded OpenMath Lean theorems locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bennyzhe](https://clawhub.ai/user/bennyzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare a local Lean theorem workspace, check the Lean toolchain and required proof skills, iterate on proofs, and verify the final build before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer guidance may place mutable third-party Lean skills into active agent skill directories.

Mitigation: Pin and verify the leanprover-skills package and repository commit, install into a staging or project-local directory first, and inspect copied skill files before active use.

Risk: The OPENMATH_LEAN_SKILL_REPO_URL override can redirect the source used for auto-install.

Mitigation: Do not set OPENMATH_LEAN_SKILL_REPO_URL unless the repository is fully trusted and reviewed.

Risk: Auto-install changes the selected skill directory by cloning and copying external skill files.

Mitigation: Use auto-install only with an explicit install directory and prefer project-local paths for review before broader deployment.

## Reference(s):

- [OpenMath Lean Workspace Preflight](references/preflight.md)
- [OpenMath Lean Proof Playbook](references/proof_playbook.md)
- [Lean Language Specification](references/languages.md)
- [leanprover/skills](https://github.com/leanprover/skills)
- [OpenMath Lean Theorem on ClawHub](https://clawhub.ai/bennyzhe/skills/openmath-lean-theorem)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and Lean code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local commands that inspect or modify Lean workspaces and may guide installation of external proof skills.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence; artifact frontmatter says v1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
