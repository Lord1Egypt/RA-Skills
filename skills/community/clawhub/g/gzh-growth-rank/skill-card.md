## Description:

每日账号推荐速览直接对接官方最具“黑马体质”的阅读增长榜单，按日期查看公众号阅读增长率TOP榜。

This skill is ready for commercial/non-commercial use.

## Publisher:

[if530770](https://clawhub.ai/user/if530770)

### License/Terms of Use:

MIT-0

## Use Case:

External WeChat account operators, content editors, and researchers use this skill to fetch recent official account reading-growth rankings and analyze high-growth article patterns from real ranking output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script sends a RedFox API key to redfox.hk for authentication.

Mitigation: Use a dedicated environment variable or secret store, confirm the key scope and revocation path, and avoid sharing the key in prompts, code, logs, or output files.

Risk: If an API key is not already in the environment, the script may inspect common shell startup files.

Mitigation: Prefer setting REDFOX_API_KEY explicitly in the runtime environment and avoid granting broad home-directory file access when running the skill.

Risk: The skill may display API-provided links or Markdown exactly as received.

Mitigation: Review remote links and rendered Markdown before relying on or redistributing the output.

## Reference(s):

- [Core execution workflow](artifact/references/core_workflow.md)
- [RedFoxHub API specification](artifact/references/api-spec.md)
- [ClawHub skill page](https://clawhub.ai/if530770/skills/gzh-growth-rank)
- [RedFoxHub API endpoint](https://redfox.hk/story/api/cozeSkill/getGzhCozeSkillDataRaise)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown tables, concise prose, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranking output must be based on script stdout; analysis is limited to up to five viral-article rows, up to five content-type rows, and a 300-500 word summary when requested.]

## Skill Version(s):

1.0.5 (source: server release metadata; bundled skill frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
