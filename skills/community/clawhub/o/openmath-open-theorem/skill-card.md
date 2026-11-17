## Description:

Queries open formal verification theorems from the OpenMath platform for Lean or Rocq discovery, theorem detail lookup, and local proof workspace scaffolding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bennyzhe](https://clawhub.ai/user/bennyzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and formal verification engineers use this skill to list open OpenMath theorem bounties, inspect theorem details, and download Lean or Rocq scaffolds for local proof work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read or create an OpenMath preferences file and use configured OpenMath endpoint overrides.

Mitigation: Prefer project-local configuration, avoid storing submission or authorization fields unless needed, and only set custom endpoint environment variables when the endpoint is trusted.

Risk: Downloaded Lean or Rocq theorem source comes from a remote service and may affect local build or proof workflows.

Mitigation: Review downloaded theorem source and scaffold files before compiling, proving, or submitting work.

## Reference(s):

- [Init Setup](references/init-setup.md)
- [OpenMath Reward System](references/reward_overview.md)
- [OpenMath Platform](https://openmath.shentu.org)
- [OpenMath API Host](https://openmath-be.shentu.org)
- [mathlib4](https://github.com/leanprover-community/mathlib4.git)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated Lean or Rocq workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create OpenMath preference JSON and theorem workspace files after setup; contacts the documented OpenMath API.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports v1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
