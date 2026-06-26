## Description: <br>
GhostShield helps users analyze and obfuscate repository style signals, sensitive data, and optional watermarks to reduce AI style distillation risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[13770626440](https://clawhub.ai/user/13770626440) <br>

### License/Terms of Use: <br>
GPL-3.0 <br>


## Use Case: <br>
Developers, open source contributors, compliance teams, and employees use GhostShield to scan code or document repositories for style and privacy exposure, then generate protected copies with configurable obfuscation levels. It supports analysis, PII redaction, style-signal reduction, optional watermarking, and post-processing evaluation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository rewriting can alter code behavior or produce output that is not safe to publish without review. <br>
Mitigation: Run GhostShield on a disposable clone or separate output directory, review diffs, and run tests before publishing or relying on transformed code. <br>
Risk: Level 3 processing and watermarking can add invisible markers or adversarial style noise to files. <br>
Mitigation: Use Level 3 and watermarking only when those markers are intentionally needed, and inspect generated files before sharing. <br>
Risk: Automated PII and sensitive-data detection may miss some repository-specific secrets or identifiers. <br>
Mitigation: Treat automated redaction as a first pass and perform manual review for sensitive repositories before distribution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/13770626440/ghostshield) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [Python downloads](https://www.python.org/downloads/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI examples, analysis reports, and rewritten repository files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally against user-selected files or repositories and can write transformed copies to a separate output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
