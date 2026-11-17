## Description:

Publishes Markdown articles to a Hugo or static-site blog by generating post files, front matter, taxonomy mapping files, and optional Git commit and push commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content maintainers use this skill to turn Markdown drafts into static-site blog posts with appropriate metadata, taxonomy files, and repository publishing steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to write files, run commands, commit changes, and push to a Git remote for a blog repository.

Mitigation: Require the agent to show the exact blog path, files to be changed, commit message, and Git remote before any write, commit, or push.

Risk: The skill may read local memory or profile files while trying to discover blog configuration.

Mitigation: Allow memory-file lookup only when local profile or configuration details are acceptable inputs for blog setup discovery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/hugo-blog)
- [Hugo documentation](https://gohugo.io/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML front matter and inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify blog content files, taxonomy index files, and Git publishing commands when authorized by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
