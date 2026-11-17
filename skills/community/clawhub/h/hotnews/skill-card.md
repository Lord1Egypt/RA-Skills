## Description:

hotnews fetches trending news and hot topics from Chinese platforms and GitHub, returning structured items with titles, URLs, rankings, and metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengzhuangpro](https://clawhub.ai/user/zhengzhuangpro)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use hotnews to list supported trend sources and fetch ranked news or hot topics from social, news, finance, developer, and GitHub sources for monitoring or downstream JSON processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill permits execution of an unpinned external npm CLI through npx, so the reviewed artifact may not fully define the code that runs.

Mitigation: Review before installing, prefer a pinned and verified hotnews package version or bundled reviewed implementation, and run npm/npx in a restricted runtime.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhengzhuangpro/skills/hotnews)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands; command results may be human-readable text or JSON arrays.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [JSON results include title, URL, optional hot metric, and rank; --limit accepts 1-50 items with a default of 10.]

## Skill Version(s):

0.1.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
