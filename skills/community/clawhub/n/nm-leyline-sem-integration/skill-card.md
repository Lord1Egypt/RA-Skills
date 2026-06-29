## Description: <br>
Provides sem semantic-diff detection, install-on-first-use, and fallback patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when building or modifying agent skills that consume git diff output, so they can prefer sem semantic diffs when available and fall back to normalized standard git diff output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may propose installing sem from a direct Linux binary download. <br>
Mitigation: Review the selected sem installation source before running install commands, prefer the Rust toolchain path when appropriate, and skip installation when standard git diff output is sufficient. <br>
Risk: Fallback diff output is file-level, and optional hunk parsing can miss renames, decorated definitions, and cross-file dependencies. <br>
Mitigation: Treat fallback impact analysis as review guidance rather than complete dependency analysis; use sem when entity-level accuracy is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-leyline-sem-integration) <br>
- [Homepage metadata](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [sem project](https://github.com/Ataraxy-Labs/sem) <br>
- [sem Linux binary download referenced by install guidance](https://github.com/Ataraxy-Labs/sem/releases/latest/download/sem-x86_64-unknown-linux-gnu) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes sem detection, install-on-first-use prompts, semantic diff fallback normalization, and impact-analysis fallback guidance.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
