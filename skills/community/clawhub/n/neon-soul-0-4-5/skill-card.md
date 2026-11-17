## Description:

Automated soul synthesis for AI agents. Extracts identity from memory files, promotes recurring patterns to axioms (N>=3), generates SOUL.md with full provenance tracking. Bundled processing engine -- no manual Q&A needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sieyer](https://clawhub.ai/user/sieyer)

### License/Terms of Use:


## Use Case:

Developers and agent users use Neon Soul to synthesize a SOUL.md identity artifact from local memory files and agent session history, then inspect status, provenance, rollback backups, and trace generated axioms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Synthesis can process private memory files and OpenClaw session history.

Mitigation: Review the memory and session sources before running, remove secrets or sensitive records, and use custom memory paths when a narrower source set is needed.

Risk: Prompts may be sent to the Ollama endpoint configured in the environment.

Mitigation: Verify OLLAMA_BASE_URL points to a local or intentionally trusted endpoint before installation or execution.

Risk: The skill writes identity artifacts and local state files, and security evidence notes it may attempt a git commit.

Mitigation: Run with --dry-run first, inspect proposed output, and keep backups or version-control review in place before accepting generated artifacts.

## Reference(s):

- [Neon Soul ClawHub Skill Page](https://clawhub.ai/sieyer/skills/neon-soul-0-4-5)
- [Live Neon Homepage](https://liveneon.ai)
- [Ollama Local Service Endpoint](http://localhost:11434)

## Skill Output:

**Output Type(s):** [markdown, json, shell commands, configuration, guidance]

**Output Format:** [SOUL.md Markdown files, JSON command results, and concise agent summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes SOUL.md and .neon-soul state or backup files; dry-run mode can preview synthesis without writing the main output.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version: 0.4.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
