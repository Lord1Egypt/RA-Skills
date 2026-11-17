## Description:

Facilitates structured multi-agent debates with opposing expert views, a referee moderator, and nine specialized council votes for balanced decision-making.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miknasbh-stack](https://clawhub.ai/user/miknasbh-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and decision-makers use this skill to frame complex choices as structured debates, compare opposing viewpoints, and receive a vote tally with concise recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Debate topics, transcripts, reports, or GitHub issues may contain confidential, regulated, or proprietary information.

Mitigation: Use the skill only after reviewing logging, repository publishing, API submission, and retention settings; avoid sensitive topics unless those controls are explicitly configured.

Risk: Installation guidance includes a sudo symlink option and workspace commands that can affect local files.

Mitigation: Prefer adding the skill script directory to PATH, choose an explicit workspace, and validate project names before initialization or execution.

Risk: Agent lifecycle cleanup and multi-agent orchestration may leave sessions or context active if the runtime integration fails.

Mitigation: Review the cleanup behavior, monitor active sessions, and verify that temporary agents and debate context are cleared after each run.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/miknasbh-stack/skills/miknas-council-of-wisdom)
- [Skill Documentation](artifact/SKILL.md)
- [Implementation Guide](artifact/IMPLEMENTATION.md)
- [Quick Start README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, prompt templates, JSON configuration examples, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces debate transcripts, vote tallies, recommendations, workspace files, monitoring templates, and optional GitHub issue content.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
