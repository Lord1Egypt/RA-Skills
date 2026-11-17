## Description:

Set up automated news digests using noisepan for signal extraction, entropia for source verification, and Hacker News blind spot detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppiankov](https://clawhub.ai/user/ppiankov)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to configure daily automated news briefs, RSS feed curation, source verification, and blind spot checks that reduce manual news browsing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install mutable third-party binaries.

Mitigation: Prefer Homebrew or pinned verified releases, verify checksums before installation, and review install commands before execution.

Risk: The Linux installation path may write to /usr/local/bin.

Mitigation: Ask before system-wide installation and offer a user-local bin directory when appropriate.

Risk: The helper workflow creates local automation and temporary HTTP serving.

Mitigation: Bind temporary servers to 127.0.0.1, use private temporary directories, and review or remove helper scripts and cron jobs when no longer needed.

## Reference(s):

- [Noisepan source repository](https://github.com/ppiankov/noisepan)
- [Entropia source repository](https://github.com/ppiankov/entropia)
- [Agent-Native CLI Convention](https://ancc.dev)
- [ClawHub skill page](https://clawhub.ai/ppiankov/skills/noisepan-digest)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, YAML, and digest table examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local setup steps, helper scripts, cron prompts, RSS configuration, and quality-filtering guidance.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
