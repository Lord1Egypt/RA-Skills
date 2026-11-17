## Description:

Analyze your Claude Code sessions to discover your developer DNA - gamified performance report with letter grades, archetypes, behavioral patterns, shadow archetype, chrono analysis, and growth tips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[umang-dabhi](https://clawhub.ai/user/umang-dabhi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Claude Code use Introspect to analyze recent local session history and generate a personalized markdown performance report covering grades, archetypes, behavioral patterns, timing analysis, and growth tips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads recent local Claude Code conversations and can create persistent plaintext reports or JSON files containing private prompt or response snippets.

Mitigation: Limit the date range and project filter before running, avoid sessions containing secrets or proprietary material, and review or delete generated report and data files when finished.

Risk: Users may rely on privacy-oriented wording and underestimate that snippets from private sessions can be written to disk.

Mitigation: Tell users before execution that local reports may include conversation snippets, and store outputs only in locations appropriate for sensitive development history.

Risk: Unpinned npx or latest-style install commands may fetch a different package version than the reviewed artifact.

Mitigation: Prefer pinned, reviewed installation commands and verify the installed package or ClawHub release version before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/umang-dabhi/skills/introspect)
- [npm Package](https://www.npmjs.com/package/@umang-boss/introspect)
- [Artifact README](artifact/README.md)
- [Package README](artifact/npm-package/README.md)
- [Declared Repository](https://github.com/umang-dabhi/introspect)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with supporting JSON session-analysis data and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local Claude Code session JSONL files, writes plaintext analysis artifacts under the configured reports directory, and prints JSON analysis data to stdout.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
