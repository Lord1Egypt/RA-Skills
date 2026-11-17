## Description:

Write a full-length technical book using multi-agent AI orchestration, spawning parallel research, writing, and review agents to produce 60K-100K+ word manuscripts and revise individual chapters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chunhualiao](https://clawhub.ai/user/chunhualiao)

### License/Terms of Use:


## Use Case:

Developers, technical authors, and engineering teams use this skill to plan, research, draft, review, and publish long-form technical books from a topic or source repository. It also supports revising individual chapters and re-integrating them into a manuscript.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can keep running later through its cron safety-net behavior.

Mitigation: Disable the cron safety-net behavior unless it is explicitly needed, and review WORKLOG.md before any resumed work.

Risk: API keys may be exposed to child processes or subagents.

Mitigation: Avoid exporting global API keys to all subagents; scope credentials to only the providers required for the current run.

Risk: The workflow can broadly commit or push repository changes.

Mitigation: Run it in a dedicated repository or branch, then review git status and diffs before any commit or push.

Risk: DeepWiki use may disclose private source material.

Mitigation: Use public repositories with DeepWiki, or get explicit approval before sending private source material to that service.

Risk: Optional dependencies can affect reproducibility.

Mitigation: Pin optional dependencies and tools such as markdown2 or pandoc when repeatable output is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chunhualiao/skills/git-repo-to-book)
- [OpenClaw](https://openclaw.ai)
- [OpenClaw Docs](https://docs.openclaw.ai)
- [The OpenClaw Paradigm Reference Implementation](https://github.com/chunhualiao/openclaw-paradigm-book)
- [Model Context Protocol](https://modelcontextprotocol.io)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown files, JSON metadata, optional HTML, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces chapter files, research notes, review files, polished manuscripts, metadata, optional HTML export, and git project history.]

## Skill Version(s):

1.0.0 (source: skill.yml, release evidence, CHANGELOG released 2026-02-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
