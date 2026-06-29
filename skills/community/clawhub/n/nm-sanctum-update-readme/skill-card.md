## Description: <br>
Refreshes README structure and content using repo context and exemplar research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to refresh README.md or another documentation file after significant project changes. It guides repository language detection, exemplar README research, outline alignment, direct documentation edits, and final verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit README.md or another documentation file based on repository context and external examples. <br>
Mitigation: Review the documentation diff, cited exemplar sources, and final verification report before merging changes. <br>
Risk: The skill has broad documentation-related triggers and relies on related Night Market capabilities when available. <br>
Mitigation: Invoke it only for explicit README refresh tasks and review the related Night Market dependencies separately in environments that support them. <br>
Risk: External README research can introduce stale, irrelevant, or unsupported patterns into project documentation. <br>
Mitigation: Require citations for exemplar-derived decisions and keep claims grounded in current repository files, tests, benchmarks, or documented reviews. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-sanctum-update-readme) <br>
- [Night Market Sanctum plugin](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>
- [Language Audit Patterns](artifact/modules/language-audit.md) <br>
- [Exemplar Research Patterns](artifact/modules/exemplar-research.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown prose with command snippets and an edited README or documentation file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include citations for external README exemplars and a final verification summary.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
