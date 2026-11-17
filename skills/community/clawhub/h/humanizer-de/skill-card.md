## Description:

Humanizer-DE analyzes German text for AI-writing patterns, vocabulary markers, statistical signals, and human-facing rewrite suggestions, with an optional offline Node.js CLI subset.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tikitackr](https://clawhub.ai/user/tikitackr)

### License/Terms of Use:

MIT-0

## Use Case:

German-speaking writers, editors, and developers use this skill to assess whether German text reads like AI-generated writing and to receive concrete scoring, flagged passages, and revision guidance. It can also rewrite text with baseline or Lesch-style humanization patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional CLI fix command writes predictable local backup and fixed-output files that may overwrite user-writable targets.

Mitigation: Review the CLI before using fix, run it only in trusted working directories, and prefer score, analyze, and suggest for routine local text review.

Risk: Humanizing rewrites can add personal-sounding details that may change meaning or factual fidelity.

Mitigation: Manually review rewritten text against the original source before publication or submission.

## Reference(s):

- [Humanizer-DE ClawHub page](https://clawhub.ai/tikitackr/skills/humanizer-de)
- [README](artifact/README.md)
- [KI-Muster](artifact/references/ki-muster.md)
- [Vokabeln](artifact/references/vokabeln.md)
- [Statistische Signale](artifact/references/statistische-signale.md)
- [Personality Injection](artifact/references/personality-injection.md)
- [Examples](artifact/references/examples.md)
- [Basis Stil-Layer](artifact/references/stil-layer/basis.md)
- [Lesch Stil-Layer](artifact/references/stil-layer/lesch.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports, inline scoring summaries, rewrite suggestions, and optional Node.js CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [German-language analysis and rewriting guidance; offline CLI mode uses local file input and output.]

## Skill Version(s):

1.3.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
