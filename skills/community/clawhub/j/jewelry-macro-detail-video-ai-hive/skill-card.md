## Description:

This skill helps jewelry, ecommerce, photography, and advertising teams turn macro jewelry video requests into reviewable production plans, prompts, runnable AI-HIVE commands, generated video tasks, and quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to produce commercial jewelry macro-detail video workflows for ecommerce, advertising, social commerce, and marketing channels. It supports production briefs, shot scripts, prompt plans, AI-HIVE generation commands, task records, and acceptance checks while preserving review before paid generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured API base URL could receive the user's AI-HIVE API key.

Mitigation: Use only the official AI-HIVE API URL and avoid setting AI_HIVE_BASE_URL or --base-url to untrusted hosts.

Risk: Media uploads or generation commands may incur costs or disclose user-provided media.

Mitigation: Confirm prompts, model parameters, routing, uploaded assets, and expected charges before running commands that submit generation jobs.

Risk: Generated jewelry videos can imply inaccurate product facts, material claims, or brand endorsements.

Mitigation: Verify gemstone grades, weights, certificates, materials, authorization, and brand claims against trusted user-provided facts before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/jewelry-macro-detail-video-ai-hive)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands, JSON task records, prompt text, production checklists, and optional local files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE task IDs, routing choices, pricing snapshots, downloaded media paths, and local blueprint JSON when the user authorizes generation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
