## Description: <br>
Queries open formal verification theorems from OpenMath, fetches theorem details, and scaffolds local Lean or Rocq proof workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bennyzhe](https://clawhub.ai/user/bennyzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and formal verification users use this skill to discover open OpenMath theorems, inspect theorem details, and create local proof scaffolds for Lean or Rocq. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper scripts contact the disclosed OpenMath service and depend on the returned theorem data. <br>
Mitigation: Use the configured OpenMath endpoints intentionally and review downloaded theorem source before running proof tools. <br>
Risk: The download workflow writes local Lean or Rocq scaffold files and can replace an existing target directory when forced. <br>
Mitigation: Prefer project-scoped configuration and avoid --force unless the output directory is safe to replace. <br>


## Reference(s): <br>
- [OpenMath Setup Flow](references/init-setup.md) <br>
- [OpenMath Reward System](references/reward_overview.md) <br>
- [OpenMath Platform](https://openmath.shentu.org) <br>
- [OpenMath API Host](https://openmath-be.shentu.org) <br>
- [mathlib4](https://github.com/leanprover-community/mathlib4.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, terminal text, JSON theorem metadata, and generated Lean or Rocq workspace files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a preferred Lean or Rocq language setting and may write local scaffold files under the selected output directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence.release.version; artifact frontmatter says v1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
