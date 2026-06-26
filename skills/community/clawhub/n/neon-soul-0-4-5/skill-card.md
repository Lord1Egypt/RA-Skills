## Description: <br>
Automated soul synthesis for AI agents that extracts identity from memory files, promotes recurring patterns to axioms, and generates SOUL.md with provenance tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sieyer](https://clawhub.ai/user/Sieyer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to synthesize a local SOUL.md identity document from memory files and session history, then inspect status, roll back backups, audit axioms, and trace provenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads personal memory files and session history to infer identity patterns. <br>
Mitigation: Review the memory directory first, remove sensitive content, and run synthesis with --dry-run before allowing writes. <br>
Risk: Generated SOUL.md and .neon-soul data may be written into a git-tracked workspace. <br>
Mitigation: Use an output path outside repository history or update ignore rules before running synthesis or scheduled cron. <br>
Risk: Scheduled synthesis can repeatedly process new personal data without an interactive review step. <br>
Mitigation: Avoid cron unless continuous processing is intended, and inspect generated files after each run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sieyer/neon-soul-0-4-5) <br>
- [NEON homepage](https://liveneon.ai) <br>
- [Ollama local service endpoint](http://localhost:11434) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes SOUL.md and .neon-soul backup, state, synthesis, and cache files unless run with --dry-run.] <br>

## Skill Version(s): <br>
0.4.5 (source: SKILL.md frontmatter and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
