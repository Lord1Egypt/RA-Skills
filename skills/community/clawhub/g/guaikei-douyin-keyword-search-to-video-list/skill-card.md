## Description:

Provides CLI-assisted access to public Douyin keyword search, creator post lists, video comments, and real-time hot lists for downstream analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, content analysts, and developers use this skill to gather public Douyin search results, creator posts, comments, and trending topics for short-video research, competitive analysis, content planning, and sentiment review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, target URLs, and fetched public Douyin data are sent to guaikei.com.

Mitigation: Use the skill only for intended Douyin research workflows and avoid submitting sensitive research targets or confidential planning terms.

Risk: A GUAIKEI_API_TOKEN is required for execution.

Mitigation: Store the token in the environment, restrict access to it, and rotate it promptly if it is exposed.

Risk: Fetched results are saved under the skill's local logs directory.

Mitigation: Review and clear local logs when they contain sensitive queries, creator targets, comments, or analysis inputs.

Risk: The activation language may trigger the skill for broad short-video research tasks even when Douyin is not named.

Mitigation: Confirm that the requested workflow is specifically intended for Douyin data before running the CLI.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-keyword-search-to-video-list)
- [Publisher Profile](https://clawhub.ai/user/engheng-art)
- [GUAIKEI Token and Support Site](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)
- [CLI Request and Response Schemas](assets/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; executed CLI tools return JSON and write local JSON logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a GUAIKEI_API_TOKEN; supports search, post, comment, and hot-list commands.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, changelog, and runtime constants)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
